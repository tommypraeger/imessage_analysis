def initialize_result_dict(member_name, df, result_dict):# Add names if not already there
    if member_name not in result_dict['names']:
        result_dict['names'].append(member_name)

    total_messages = len(
        df[df['sender'] == member_name]
    )
    non_reaction_messages = len(
        df[(df['sender'] == member_name) & (~df['is reaction?'])]
    )
    try:
        assert(total_messages > 0)
        assert(non_reaction_messages > 0)
    except AssertionError:
        raise Exception('Somebody in this chat hasn\'t sent a message yet. Aborting.')
    
    return total_messages, non_reaction_messages
