SELECT
    g.room_id,
    g.highest_bid,
    g.stake,
    landlord.public_player_id,
    p1.public_player_id,
    p2.public_player_id,
    g.landlord_won
FROM games g
JOIN players landlord ON landlord.player_id = g.landlord_id
JOIN players p1       ON p1.player_id       = g.player_1_id
JOIN players p2       ON p2.player_id       = g.player_2_id
WHERE array_sort(ARRAY[landlord.public_player_id, p1.public_player_id, p2.public_player_id])
    = array_sort(ARRAY[%s, %s, %s]);