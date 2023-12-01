track_index = []
track_index_data = []

not_found = []

blocks = []
l_blocks = 0

def trackBlocked(paths, dimension):
    global track_index
    global track_index_data

    global not_found

    global blocks

    if (not (paths in track_index or paths in not_found)) or True:
        # go through all blocks
        for b in l_blocks:
            # check if block is not occupied and not reserved
            if not ( blocks[b]["occupied"] or blocks[b]["reserved"] ): continue
            # next up, go through all segments
            segments = blocks[b]["segments"]
            for s in segments:
                # check if segment is in current dimension
                if s["dimension"] != dimension: continue
                # next, see if  segment has correct path
                if s["path"] == paths:
                    # add path to index
                    #track_index.append(paths)
                    #track_index_data.append(b)
                    # check if track is occupied
                    if blocks[b]["occupied"]:
                        return "O"
                    # or it is reserved
                    elif blocks[b]["reserved"]:
                        return "R"
        not_found.append(paths)
    elif paths in track_index:
        # get block
        b = blocks[ track_index_data[ track_index.index(paths) ] ]
        # check if track is occupied
        if b["occupied"]:
            return "O"
        # or it is reserved
        elif b["reserved"]:
            return "R"
    return None