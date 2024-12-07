(define (problem garage-problem)
    (:domain garage)

    (:objects
        assistant - robot
        assistant_base_location - location
        
        girl - worker
        girl_location - location
        
        tape - tape
        tape_location - location

        mass - piece
        mass_location - location

        handle - piece
        handle_location - location

        hammer - hammer
        hammer_location - location

        screwdiver - screwdiver 
        screwdiver_location - location

        screwdiver_piece - piece
        screwdiver_piece_location - location

        uselesstool - tool
        uselesstool_location - location

        uselesspiece1 - piece
        uselesspiece1_location - location

        uselesspiece2 - piece
        uselesspiece2_location - location

        uselesspiece3 - piece
        uselesspiece3_location - location

    )

    (:init
        (at assistant assistant_base_location) 
        (at tape tape_location)
        (at girl girl_location)
        (at mass mass_location)
        (at handle handle_location)
        (at hammer hammer_location)
        (at screwdiver screwdiver_location)
        (at screwdiver_piece screwdiver_piece_location)
        (at uselesstool uselesstool_location)
        (at uselesspiece1 uselesspiece1_location)
        (at uselesspiece2 uselesspiece2_location)
        (at uselesspiece3 uselesspiece3_location)
        (is_screwdiver_piece screwdiver_piece)
        (is_hammer_piece1 mass)
        (is_hammer_piece2 handle)
        (holding_0 assistant)
        
    )

    (:goal
        (and
            (has girl tape)     
            (works hammer)
            (has girl hammer)    
            (works screwdiver)
            (has girl screwdiver)
        )
    )
)
