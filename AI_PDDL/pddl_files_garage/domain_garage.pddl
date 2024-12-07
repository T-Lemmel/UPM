(define (domain garage)

    (:requirements :typing :negative-preconditions :disjunctive-preconditions :equality :conditional-effects)

    (:types 
        location locatable - object
        worker - locatable
        pickable - locatable
        robot - locatable
        tool - pickable
        piece - pickable
        hammer - tool
        screwdiver - tool
        tape - tool
    )

    (:predicates 
        (at ?obj - locatable ?loc - location) ; location of a locatable object
        (has ?girl - worker ?tool - tool)
        (holding ?assistant - robot ?held - locatable) ; robot holding a locatable object
        (works ?tested_tool - tool) ; tool is working, no need to repair
        (is_hammer_piece1 ?tested_piece - piece) ; object is hammer piece 1
        (is_hammer_piece2 ?tested_piece - piece) ; object is hammer piece 2
        (is_screwdiver_piece ?tested_piece - piece) ; object is screwdiver piece
        (holding_0 ?assistant - robot) ; robot is holding 0 objects
        (holding_1 ?assistant - robot) ; robot is holding 1 object
        (holding_2 ?assistant - robot) ; robot is holding 2 objects
        (holding_3 ?assistant - robot) ; robot is holding 3 objects
    )

    (:action go-to
        :parameters 
            (?assistant - robot
             ?from - location
             ?to - location) 
        :precondition
            (at ?assistant ?from) ; The robot is at the starting location.            
        :effect
            (and 
                (at ?assistant ?to) ; The robot is now at the destination location.
                (not (at ?assistant ?from)) ; The robot is no longer at the starting location.
            )
    )

    (:action assistant-pick-up
    :parameters 
        (?assistant - robot
         ?to_pick_up - pickable
         ?location - location) 
    :precondition
        (and 
            (at ?assistant ?location)       ; The robot is at the location.
            (at ?to_pick_up ?location)      ; The object to pick up is at the location.
            (or (holding_0 ?assistant)
                (holding_1 ?assistant)
                (holding_2 ?assistant))     ; The robot can hold up to 3 objects.
        )            
    :effect
        (and 
            (holding ?assistant ?to_pick_up) ; The robot is now holding the object.
            (not (at ?to_pick_up ?location)) ; The object is no longer at the location.
            
            ; Update the holding state
            (when (holding_0 ?assistant) (and (not (holding_0 ?assistant)) (holding_1 ?assistant)))
            (when (holding_1 ?assistant) (and (not (holding_1 ?assistant)) (holding_2 ?assistant)))
            (when (holding_2 ?assistant) (and (not (holding_2 ?assistant)) (holding_3 ?assistant)))
        )
    )

    (:action repair_hammer
    :parameters 
        (?assistant - robot
         ?hammer_to_repair - hammer
         ?piece1 - piece
         ?piece2 - piece
         ?location - location)

    :precondition
        (and
            (at ?assistant ?location)
            (holding ?assistant ?hammer_to_repair)
            (holding ?assistant ?piece1)
            (holding ?assistant ?piece2)
            (is_hammer_piece1 ?piece1)
            (is_hammer_piece2 ?piece2)
        )
    :effect
        (and
            (works ?hammer_to_repair)                    ; The tool is now repaired.
            (not (holding ?assistant ?piece1))
            (not (holding ?assistant ?piece2))
            (at ?piece1 ?location)
            (at ?piece2 ?location)

            ; Update the holding count
            (when (holding_3 ?assistant) (and (not (holding_3 ?assistant)) (holding_1 ?assistant)))
            (when (holding_2 ?assistant) (and (not (holding_2 ?assistant)) (holding_0 ?assistant)))
        )
    )


    (:action repair_screwdiver
    :parameters 
        (?assistant - robot
         ?screwdiver_to_repair - screwdiver
         ?piece - piece
         ?location - location)

    :precondition
        (and
            (at ?assistant ?location)
            (holding ?assistant ?screwdiver_to_repair)
            (holding ?assistant ?piece)
            (is_screwdiver_piece ?piece)
        )
    :effect
        (and
            (works ?screwdiver_to_repair)                    ; The tool is now repaired.
            (not (holding ?assistant ?piece))
            (at ?piece ?location)

            ; Update the holding count
            (when (holding_3 ?assistant) (and (not (holding_3 ?assistant)) (holding_2 ?assistant)))
            (when (holding_2 ?assistant) (and (not (holding_2 ?assistant)) (holding_1 ?assistant)))
            (when (holding_1 ?assistant) (and (not (holding_1 ?assistant)) (holding_0 ?assistant)))
        )
    )


    (:action assistant-put-down 
    :parameters 
        (?assistant - robot
         ?to_put_down - locatable
         ?location - location) 
    :precondition
        (and 
            (holding ?assistant ?to_put_down) ; The robot is holding the object.
            (at ?assistant ?location)         ; The robot is at the location.
        )            
    :effect
        (and 
            (at ?to_put_down ?location)       ; The object is now at the location.
            (not (holding ?assistant ?to_put_down)) ; The robot is no longer holding the object.

            ; Update the holding state
            (when (holding_1 ?assistant) (and (not (holding_1 ?assistant)) (holding_0 ?assistant)))
            (when (holding_2 ?assistant) (and (not (holding_2 ?assistant)) (holding_1 ?assistant)))
            (when (holding_3 ?assistant) (and (not (holding_3 ?assistant)) (holding_2 ?assistant)))
        )
)


    (:action worker-pick-up        
        :parameters
            (?girl - worker
             ?tool - tool
             ?location - location)
        :precondition
            (and
                (at ?girl ?location) ;
                (at ?tool ?location) ;
            )
        :effect
            (and
                (has ?girl ?tool) ;
                (not (at ?tool ?location)) ;
            )
    )
)
