"""Aldreth skill-tree engine: bonus DSL -> Passive Skill Tree 0.7.6 JSON, radial layout, descriptions, validation helpers.

Conventions
-----------
Bonus builders return (json_dict, text). Node ids: aldreth:<region>_<slot>. Attribute modifier UUIDs are deterministic (uuid5).
Operations: 0 = ADD, 1 = MULTIPLY_BASE (+x%), 2 = MULTIPLY_TOTAL.
Conditions (single, PST has no AND): "hp>0.8" "hp<0.35" "missinghp>0.3" "food>0.5" "sneak" "stand" "burning" "underwater" "unarmed" "dual"
  "hand:<item tag>" (item in main hand matches tag)  "worn:<equipment_type>" (shield|helmet|chestplate|leggings|boots|armor...)
  "eff:<effect id>" "effects>N" (beneficial effects count)  "debuffs>N"
Multipliers ("per"): "missinghp/0.1" (per 10% missing health) "hp/0.1" "armor/4" "maxhp/10" "effects/1" "debuffs/1" "food/0.1" "skills/10" "dist/4"
"""
import hashlib, json, math, uuid

NS = "aldreth"
NONE = {"type": "skilltree:none"}


def _uuid(seed):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "aldreth/" + seed))


def provider(name):
    if name == "hp":
        return {"type": "skilltree:health_level", "percentage": True, "missing": False}
    if name == "missinghp":
        return {"type": "skilltree:health_level", "percentage": True, "missing": True}
    if name == "food":
        return {"type": "skilltree:food_level", "percentage": True, "missing": False}
    if name == "armor":
        return {"type": "skilltree:attribute_value", "attribute": "minecraft:generic.armor"}
    if name == "maxhp":
        return {"type": "skilltree:attribute_value", "attribute": "minecraft:generic.max_health"}
    if name == "effects":
        return {"type": "skilltree:effect_amount", "effect_type": "beneficial"}
    if name == "debuffs":
        return {"type": "skilltree:effect_amount", "effect_type": "harmful"}
    if name == "skills":
        return {"type": "skilltree:learned_skills_amount"}
    if name == "dist":
        return {"type": "skilltree:distance_to_target"}
    if name.startswith("attr:"):
        return {"type": "skilltree:attribute_value", "attribute": name[5:]}
    raise ValueError("provider " + name)


def per(spec):
    if not spec:
        return NONE
    name, div = spec.split("/")
    return {"type": "skilltree:numeric_value", "divisor": float(div), "value_provider": provider(name)}


LOGIC = {">": "MORE", "<": "LESS", ">=": "AT_LEAST", "<=": "AT_MOST", "=": "EQUAL"}


def cond(spec):
    """Living-entity (player/target) condition."""
    if not spec or spec == "none":
        return NONE
    for head, name in (("missinghp", "missinghp"), ("hp", "hp"), ("food", "food"), ("effects", "effects"), ("debuffs", "debuffs"), ("dist", "dist")):
        if spec.startswith(head) and len(spec) > len(head) and spec[len(head)] in "<>=":
            op = spec[len(head)]
            rest = spec[len(head) + 1:]
            if rest.startswith("="):
                op += "="
                rest = rest[1:]
            return {"type": "skilltree:numeric_value", "logic": LOGIC[op], "required_value": float(rest), "value_provider": provider(name)}
    if spec == "sneak":
        return {"type": "skilltree:crouching", "reverse_logic": False}
    if spec == "stand":
        return {"type": "skilltree:crouching", "reverse_logic": True}
    if spec in ("burning", "underwater", "unarmed", "dual_wielding", "fishing"):
        return {"type": "skilltree:" + spec}
    if spec == "dual":
        return {"type": "skilltree:dual_wielding"}
    if spec.startswith("hand:"):
        return {"type": "skilltree:has_item_in_hand", "item_condition": {"type": "skilltree:tag", "tag_id": spec[5:]}}
    if spec.startswith("handtype:"):
        return {"type": "skilltree:has_item_in_hand", "item_condition": {"type": "skilltree:equipment_type", "equipment_type": spec[9:]}}
    if spec.startswith("worn:"):
        return {"type": "skilltree:has_item_equipped", "item_condition": {"type": "skilltree:equipment_type", "equipment_type": spec[5:]}}
    if spec.startswith("eff:"):
        return {"type": "skilltree:has_effect", "effect": spec[4:], "amplifier": 0}
    raise ValueError("cond " + spec)


def dcond(spec):
    """Damage-source condition."""
    if not spec or spec in ("any", "none"):
        return NONE
    if spec in ("melee", "projectile", "magic", "fire", "fall", "poison", "thorns"):
        return {"type": "skilltree:" + spec}
    raise ValueError("dcond " + spec)


class Ctx:
    """Collects bonuses for one node, assigns deterministic UUIDs."""

    def __init__(self, node_id):
        self.node_id = node_id
        self.n = 0

    def uid(self):
        self.n += 1
        return _uuid("%s/%d" % (self.node_id, self.n))


def pct(x):
    return ("%+.1f%%" % (x * 100)).replace(".0%", "%")


# ---- bonus builders: each returns f(ctx) -> (json, text) ---------------------------------------------------------------
def A(attribute, amount, op=0, when=None, by=None, label=None):
    def f(c):
        j = {"type": "skilltree:attribute", "attribute": attribute, "id": c.uid(), "name": "Aldreth", "amount": amount, "operation": op,
             "player_multiplier": per(by), "player_condition": cond(when)}
        nm = label or attribute.split(":")[1].split(".")[-1].replace("_", " ")
        t = ("%s %s" % (pct(amount) if op else "%+g" % amount, nm))
        return j, _suffix(t, when, by)
    return f


def D(amount, kind="any", when=None, by=None, target=None, enemy_by=None, op=1, label=None):
    def f(c):
        j = {"type": "skilltree:damage", "amount": amount, "operation": op, "player_multiplier": per(by), "enemy_multiplier": per(enemy_by),
             "player_condition": cond(when), "damage_condition": dcond(kind), "target_condition": cond(target)}
        t = "%s %sdamage" % (pct(amount), "" if kind == "any" else kind + " ")
        return j, _suffix(t, when, by, target)
    return f


def T(amount, kind="any", when=None, by=None, label=None):
    """Damage TAKEN (negative = reduction)."""
    def f(c):
        j = {"type": "skilltree:damage_taken", "amount": amount, "operation": 1, "player_multiplier": per(by), "attacker_multiplier": NONE,
             "player_condition": cond(when), "damage_condition": dcond(kind), "attacker_condition": NONE}
        t = "%s %sdamage taken" % (pct(amount), "" if kind == "any" else kind + " ")
        return j, _suffix(t, when, by)
    return f


def CC(chance, when=None, by=None, target=None):
    def f(c):
        j = {"type": "skilltree:crit_chance", "chance": chance, "player_multiplier": per(by), "enemy_multiplier": NONE,
             "player_condition": cond(when), "damage_condition": NONE, "target_condition": cond(target)}
        return j, _suffix("%s critical chance" % pct(chance), when, by, target)
    return f


def CD(amount, when=None, by=None, target=None):
    def f(c):
        j = {"type": "skilltree:crit_damage", "amount": amount, "operation": 1, "player_multiplier": per(by), "enemy_multiplier": NONE,
             "player_condition": cond(when), "damage_condition": NONE, "target_condition": cond(target)}
        return j, _suffix("%s critical damage" % pct(amount), when, by, target)
    return f


def AV(chance, kind="any", when=None):
    def f(c):
        j = {"type": "skilltree:damage_avoidance", "chance": chance, "player_multiplier": NONE, "attacker_multiplier": NONE,
             "player_condition": cond(when), "damage_condition": dcond(kind), "attacker_condition": NONE}
        return j, _suffix("%s chance to avoid %sdamage" % (pct(chance), "" if kind == "any" else kind + " "), when)
    return f


def HEAL(amount, listener, chance=1.0, pct_heal=True, cooldown=20, text=None):
    """listener: 'tick' | 'kill' | 'crit' | 'hit' (on attack) | 'block' | 'evade' | 'hurt'."""
    def f(c):
        j = {"type": "skilltree:healing", "chance": chance, "amount": amount, "event_listener": _listener(listener, cooldown),
             "percentage_healing": pct_heal}
        t = text or "Heal %s%s %s" % ("%g" % (amount * 100) if pct_heal else "%g" % amount, "% of max health" if pct_heal else " health", _ev(listener, chance, cooldown))
        return j, t
    return f


def FX(effect, seconds, amp, listener, chance=1.0, target="enemy", cooldown=None, stacks=0):
    def f(c):
        j = {"type": "skilltree:inflict_effect", "chance": chance, "max_stacks": stacks, "effect": effect, "duration": int(seconds * 20), "amplifier": amp,
             "event_listener": _listener(listener, cooldown or 20, target)}
        who = {"enemy": "the enemy", "player": "you"}[target]
        t = "%s%s %s for %gs on %s" % ("%g%% chance: " % (chance * 100) if chance < 1 else "", effect.split(":")[1].replace("_", " ").title() + (" %d" % (amp + 1) if amp else ""), "" if target == "enemy" else "on you", seconds, _evn(listener))
        return j, t.replace("  ", " ") + (" (%s)" % who if False else "")
    return f


def CMD(command, listener, desc, cooldown=20, chance=None):
    def f(c):
        j = {"type": "skilltree:command", "command": command, "description": desc, "event_listener": _listener(listener, cooldown)}
        return j, "%s (%s)" % (desc, _evn(listener))
    return f


def REGEN(amount, cooldown=40):
    return HEAL(amount, "tick", cooldown=cooldown)


def XP(mult, source="any"):
    def f(c):
        j = {"type": "skilltree:gained_experience", "multiplier": mult, "experience_source": source, "player_multiplier": NONE}
        return j, "%s %s experience" % (pct(mult), source if source != "any" else "all")
    return f


def LOOT(chance, kind="mobs", mult=1.0):
    def f(c):
        j = {"type": "skilltree:loot_duplication", "chance": chance, "multiplier": mult, "loot_type": kind}
        return j, "%s chance to duplicate %s loot" % (pct(chance), kind)
    return f


def JUMP(mult, when=None):
    def f(c):
        return {"type": "skilltree:jump_height", "multiplier": mult, "player_condition": cond(when)}, _suffix("%s jump height" % pct(mult), when)
    return f


def PSPEED(mult, when=None):
    def f(c):
        return {"type": "skilltree:projectile_speed", "multiplier": mult, "player_multiplier": NONE, "player_condition": cond(when)}, _suffix("%s projectile speed" % pct(mult), when)
    return f


def PDUP(chance, when=None):
    def f(c):
        return {"type": "skilltree:projectile_duplication", "chance": chance, "player_multiplier": NONE, "player_condition": cond(when)}, _suffix("%s chance to fire an extra projectile" % pct(chance), when)
    return f


def ARROW(chance):
    def f(c):
        return {"type": "skilltree:arrow_retrieval", "chance": chance}, "%s chance to retrieve fired arrows" % pct(chance)
    return f


def IGNITE(chance, seconds=4, listener="hit"):
    def f(c):
        return {"type": "skilltree:inflict_ignite", "chance": chance, "duration": seconds, "event_listener": _listener(listener, 20, "enemy")}, "%s chance to ignite enemies for %ds %s" % (pct(chance), seconds, _evn(listener))
    return f


def HEALTAKEN(mult, when=None):
    def f(c):
        return {"type": "skilltree:incoming_healing", "multiplier": mult, "player_multiplier": NONE, "player_condition": cond(when)}, _suffix("%s healing received" % pct(mult), when)
    return f


def USESPEED(mult, when=None):
    def f(c):
        return {"type": "skilltree:item_usage_speed", "multiplier": mult, "player_multiplier": NONE, "player_condition": cond(when)}, _suffix("%s item use speed" % pct(mult), when)
    return f


def NOUSE(tag):
    """Drawback: cannot use items of a tag (e.g. aldreth:weapons/ranged)."""
    def f(c):
        return {"type": "skilltree:cant_use_item", "item_condition": {"type": "skilltree:tag", "tag_id": tag}}, "Cannot use %s" % tag.split("/")[-1].replace("_", " ") + " weapons"
    return f


def RESERVE(amount):
    def f(c):
        return {"type": "skilltree:health_reservation", "amount": amount, "player_multiplier": NONE, "player_condition": NONE}, "Reserves %s of maximum health" % pct(amount).replace("+", "")
    return f


def CONVERT(amount, src, dst):
    def f(c):
        return {"type": "skilltree:damage_conversion", "amount": amount, "original_damage": dcond(src), "result_damage": dcond(dst),
                "player_multiplier": NONE, "enemy_multiplier": NONE, "player_condition": NONE, "target_condition": NONE}, "Convert %s of %s damage to %s" % (pct(amount).replace("+", ""), src, dst)
    return f


def STEALTH(amount):
    def f(c):
        return {"type": "skilltree:stealth", "amount": amount, "player_multiplier": NONE, "enemy_multiplier": NONE, "player_condition": NONE, "target_condition": NONE}, "%s stealth" % pct(amount)
    return f


def NOIMMUNE_POISON(chance):
    def f(c):
        return {"type": "skilltree:lethal_poison"}, "Poison can be lethal"
    return f


# ---- helpers -----------------------------------------------------------------------------------------------------------
_EV = {"tick": "every second", "kill": "on kill", "crit": "on critical hit", "hit": "on hit", "block": "on shield block", "evade": "on evasion", "hurt": "when hurt"}


def _ev(listener, chance, cooldown):
    s = _EV[listener]
    return ("%s (%g%% chance)" % (s, chance * 100)) if chance < 1 else s


def _evn(listener):
    return _EV.get(listener, listener)


def _listener(name, cooldown=20, target="enemy"):
    if name == "tick":
        return {"type": "skilltree:ticking", "cooldown": cooldown, "player_condition": NONE, "player_multiplier": NONE}
    if name == "kill":
        return {"type": "skilltree:on_kill", "damage_condition": NONE, "enemy_condition": NONE, "player_condition": NONE, "enemy_multiplier": NONE, "player_multiplier": NONE}
    if name == "crit":
        return {"type": "skilltree:critical_hit", "target": target, "enemy_condition": NONE, "player_condition": NONE, "enemy_multiplier": NONE, "player_multiplier": NONE}
    if name == "hit":
        return {"type": "skilltree:attack", "target": target, "damage_condition": NONE}
    if name == "block":
        return {"type": "skilltree:block", "target": target, "enemy_condition": NONE, "player_condition": NONE, "enemy_multiplier": NONE, "player_multiplier": NONE}
    if name == "evade":
        return {"type": "skilltree:evasion", "target": target, "enemy_condition": NONE, "player_condition": NONE, "enemy_multiplier": NONE, "player_multiplier": NONE}
    if name == "hurt":
        return {"type": "skilltree:damage_taken", "target": target, "damage_condition": NONE}
    raise ValueError(name)


def _suffix(t, when=None, by=None, target=None):
    names = {"hp>": "above %d%% health", "hp<": "below %d%% health"}
    extra = []
    if when:
        w = when
        if w.startswith("hp>"):
            extra.append("while above %d%% health" % round(float(w[3:]) * 100))
        elif w.startswith("hp<"):
            extra.append("while below %d%% health" % round(float(w[3:]) * 100))
        elif w.startswith("hand:"):
            extra.append("while wielding %s" % w.split("/")[-1])
        elif w.startswith("worn:"):
            extra.append("while wearing/holding a %s" % w[5:])
        elif w.startswith("missinghp>"):
            extra.append("while missing %d%%+ health" % round(float(w[10:]) * 100))
        else:
            extra.append("while " + w)
    if target:
        extra.append("against targets: " + target)
    if by:
        n, d = by.split("/")
        extra.append("per %s %s" % (d, n))
    return t + (" " + ", ".join(extra) if extra else "")


# ---- node model + layout -----------------------------------------------------------------------------------------------
KIND_VIS = {
    "minor": ("lesser", 16), "notable": ("notable", 24), "major": ("notable", 28), "mastery": ("notable", 30),
    "keystone": ("keystone", 36), "entry": ("gateway", 24), "bridge": ("notable", 24), "start": ("gateway", 32),
}
RING_SIZES = [3, 4, 5, 6, 6, 6, 5, 4, 3]
RING_TYPES = ["m E m", "m m m m", "m N m N m", "m m N m m N", "m M m m M m", "m N m M m N", "N M N M m", "S S S S", "K K K"]
RING_R0, RING_STEP = 175.0, 78.0


def node_json(nid, title, kind, icon, bonuses, x, y, links, start=False, color=""):
    bg, size = KIND_VIS[kind]
    ctx = Ctx(nid)
    js, tx = [], []
    for b in bonuses:
        j, t = b(ctx)
        js.append(j)
        tx.append(t)
    return {
        "id": nid, "title": title, "titleColor": color, "bonuses": js, "requirements": [], "directConnections": sorted(links),
        "longConnections": [], "oneWayConnections": [], "tags": [],
        "backgroundTexture": "skilltree:textures/icons/background/%s.png" % bg, "iconTexture": icon,
        "borderTexture": "skilltree:textures/tooltip/%s.png" % ("keystone" if kind == "keystone" else "notable" if bg == "notable" else "gateway" if bg == "gateway" else "lesser"),
        "buttonSize": size, "isStartingPoint": start, "positionX": round(x, 2), "positionY": round(y, 2),
    }, tx
