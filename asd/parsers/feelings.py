import json

def parse_feelings(context, snapshot):
    feelings_obj = dict(hunger=snapshot.feelings.hunger,
                        thirst=snapshot.feelings.thirst,
                        exhaustion=snapshot.feelings.exhaustion,
                        happiness=snapshot.feelings.happiness
                        )
    res = json.dumps(feelings_obj)
    context.save('feelings.json', res)
    return  res

parse_feelings.field = "feelings"
