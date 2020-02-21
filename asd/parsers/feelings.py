import json

def parse_feelings(context, snapshot):
    feelings_obj = dict(hunger=snapshot.feelings.hunger,
                        thirst=snapshot.feelings.thirst,
                        exhaustion=snapshot.feelings.exhaustion,
                        happiness=snapshot.feelings.happiness
                        )
    context.save('feelings.json', json.dumps(feelings_obj))

parse_feelings.field = "feelings"
