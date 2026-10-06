import json,urllib.request,urllib.parse,sys
UA={'User-Agent':'ClaudeRPG-packbuilder/0.1 (connorhalljames@gmail.com)'}
for q in sys.argv[1:]:
    fac=json.dumps([["project_type:mod"],["categories:forge"],["versions:1.20.1"]])
    u='https://api.modrinth.com/v2/search?'+urllib.parse.urlencode({'query':q,'facets':fac,'limit':4})
    r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30))
    print('##',q,' | '.join('%s(%s,%dk)'%(h['slug'],h['title'][:28],h['downloads']//1000) for h in r['hits']))
