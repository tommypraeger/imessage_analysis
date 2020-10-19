import analysis.functions.all_caps as all_caps
import analysis.functions.attachment as attachment
import analysis.functions.convo_starter as convo_starter
import analysis.functions.emoji as emoji
import analysis.functions.frequency as frequency
import analysis.functions.game as game
import analysis.functions.link as link
import analysis.functions.message_series as message_series
import analysis.functions.mime_type as mime_type
import analysis.functions.phrase as phrase
import analysis.functions.reaction as reaction
import analysis.functions.total as total
import analysis.functions.tweet as tweet
import analysis.functions.word_count as word_count
import analysis.functions.word_length as word_length


def process_df(df, args):
    function = args.function
    
    result_dict = {
        'names': []
    }
    
    if function == 'total' or args.all_functions:
        total.main(result_dict, df)

    if function == 'reaction' or args.all_functions:
        reaction.main(result_dict, df)

    if function == 'attachment' or args.all_functions:
        attachment.main(result_dict, df)

    if function == 'emoji' or args.all_functions:
        emoji.main(result_dict, df)

    if function == 'all_caps' or args.all_functions:
        all_caps.main(result_dict, df)

    if function == 'convo_starter' or args.all_functions:
        convo_starter.main(result_dict, df)

    if function == 'tweet' or args.all_functions:
        tweet.main(result_dict, df)

    if function == 'link' or args.all_functions:
        link.main(result_dict, df)

    if function == 'word_count' or args.all_functions:
        word_count.main(result_dict, df, args.all_functions)

    if function == 'word length' or args.all_functions:
        word_length.main(result_dict, df, args.all_functions)

    if function == 'message series' or args.all_functions:
        message_series.main(result_dict, df, args.all_functions)

    if function == 'game' or args.all_functions:
        game.main(result_dict, df)

    if function == 'frequency':
        frequency.main(result_dict, df, args)

    if function == 'phrase':
        phrase.main(result_dict, df, args.phrase, args.case_sensitive, args.separate)

    if function == 'mime_type':
        mime_type.main(result_dict, df, args.mime_type)

    return result_dict
