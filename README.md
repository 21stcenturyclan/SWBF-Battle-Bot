# SWBF Battle Bot

## TOC
- [Introduction](#introduction)
- [HowTo](#howto)
- [Missing/TODO](#missing)
- [Improvements](#improvements)

## Introduction 
<div id="introduction"></div>

This bot should help to organize battles for the [swbfgamers.com](swbfgamers.com) leaderboard.

## HowTo
<div id="howto"></div>

### Organize a battle
Everybody can organize a battle. 
For this you have to send the following command to the bot.

> `!battle <date> <time> <sizes>`

Examples:

> `!battle 15.05.2020 15:00 3,4`
>
This battle would be schedules on the 15th of may 2020 at 15:00 CEST and would allow 3v3's and 4v4's.

> `!battle 4.7 20:30`
>
This battle would be schedules on the 4th of july in the year that command was posted at 20:30 CEST and would allow 2v2's, 3v3's, 4v4's, and 5v5's.

> `!battle 17:30 2`
>
This battle would be schedules on the day that command was posted at 17:30 CEST and would allow 2v2's.
    
### Participate in a battle
If you decide to take part in a battle you have to react to the organizers invitation message with the designated emojis for the sizes of the matches.
If the match only allows 2v2 it only matters if you react with the ':2v2:' emoji.

If the match allows all types of matches you only have to react with the emojis of the type of battle you would like to take part in.
For example if you only want to play 4v4 or 5v5 you should only react with ':4v4:' and ':5v5:'.

### Start a battle
Only admins can start a battle.
When an admin reacts with the designated emoji (:+1:) the bot will do the matchmaking for the players that joined the battle.
It is possible that no battle will happen if not enough players joined the invitation or the ones that joined have different preferences.
For example, if only 7 players voted to have a 4v4 it is not possible to do 4v4.
Also if 9 players voted to have a 3v3, 3 players miss out on the battle.
Therefore it is usually recommended to join all the available battle sizes.

When the admin has given his approval the bot will create channels for each team of the battles and assign roles for each team members.
In each team there is one 'commander' role that is responsible for taking screenshots of the results and reporting it back to the bot.

#### Matchmaking
The bot's matchmaking system follows 2 optimizations:
- Create as many matches es possible
- Maximize the amount of points that players can have

Examples:

    1. 15 participants
        - Every player has given its approval for any type of battle (2v2, 3v3, 4v4, 5v5).
        -> one 3v3 and one 4v4 are scheduled
        -> 1 player misses out
        
    2. 27 participants
        - 5 players approved 2v2 and 5v5
        - 10 players approved 4v4 and 5v5
        - 7 players approved 3v3 and 4v4
        - 5 players approved 3v3, 5v5
        -> Numbers for matches: 2v2: 5 | 3v3: 12 | 4v4: 17 | 5v5: 20 
            -> two 4v4's are scheduled (players assigned to this match can not join others anymore)
        -> Numbers for matches: 2v2: 5 | 3v3: 5 | 4v4: 1 | 5v5: 10
            -> one 5v5 is scheduled
        -> Numbers for matches: 2v2: 0 | 3v3: 0 | 4v4: 1 | 5v5: 0
            -> one player misses out 

### Report a battle
After a battle is complete one of the team's commander has to report the results to the bot.

TODO

If screenshots and stats are correct either both commanders or 50% of each teams members have to approve the result with a ':+1:' reaction.
When this is done the result is stored in in the database and the bot will respond with a message when it is done.
After this you can query your updated leaderboard stats.

## Missing / TODO
<div id="missing"></div>

- It is not possible to leave a battle once a player joined
- ...

## Improvements
<div id="improvements"></div>

-