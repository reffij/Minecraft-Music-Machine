from typing import Any

def read_header(raw_data: bytes) -> dict[str, Any]:
    res: dict[str, Any] = {}

    if raw_data[:2] == b'\x00\x00':
        print('New format')
    else:
        raise ValueError('Old format, update file to new format. Open file in nbs studio and it will be updated')

    # String Reader
    def read_string(data: bytes, start_idx: int) -> tuple[str, int]:
        len_string = int.from_bytes(data[start_idx:start_idx + 4], 
                        byteorder='little')
        start_idx += 4
        return (data[start_idx:start_idx + len_string].decode('utf-8', 
                errors='ignore'), start_idx + len_string)

    index = 2

    # NBS Version (1 byte)
    nbs_version = raw_data[index]
    print(f"nbs_version: {nbs_version}")
    res["nbs_version"] = nbs_version
    index += 1

    # Vanilla Instrument Count (1 byte)
    num_instruments = raw_data[index]
    print(f"num_instruments: {num_instruments}")
    res["num_instruments"] = num_instruments
    index += 1

    # Song Length (Short, 2 bytes)
    song_length = int.from_bytes(raw_data[index:index+2], byteorder='little')
    print(f"song_length: {song_length}")
    res["song_length"] = song_length
    index += 2

    # Layer Count (Short, 2 bytes)
    layer_count = int.from_bytes(raw_data[index:index+2], byteorder='little')
    print(f"layer_count: {layer_count}")
    res["layer_count"] = layer_count
    index += 2

    #song name (string)
    song_name, index = read_string(raw_data, index)
    print(f"song_name: {song_name}")
    res["song_name"] = song_name

    #song author (string)
    song_author, index = read_string(raw_data, index)
    print(f"song_author: {song_author}")
    res["song_author"] = song_author


    #song original author (string)
    song_original_author, index = read_string(raw_data, index)
    print(f"song_original_author: {song_original_author}")
    res["song_original_author"] = song_original_author

    #song description (string)
    song_description, index = read_string(raw_data, index)
    print(f"song_description: {song_description}")
    res["song_description"] = song_description


    #song tempo (Short, 2 bytes)
    song_tempo = int.from_bytes(raw_data[index:index+2], byteorder='little')
    print(f"song_tempo: {song_tempo}")
    res["song_tempo"] = song_tempo
    index += 2

    #auto-saving (1 byte)
    auto_saving = raw_data[index]
    print(f"auto_saving: {auto_saving}")
    res["auto_saving"] = auto_saving
    index += 1

    #auto-saving duration (1 byte)
    auto_saving_duration = raw_data[index]
    print(f"auto_saving_duration: {auto_saving_duration}")
    res["auto_saving_duration"] = auto_saving_duration
    index += 1

    #time signature (1 byte)
    time_signature = raw_data[index]
    print(f"time_signature: {time_signature}")
    res["time_signature"] = time_signature
    index += 1

    #minutes spent (int 4 bytes)
    minutes_spent = raw_data[index]
    print(f"minutes_spent: {minutes_spent}")
    res["minutes_spent"] = minutes_spent
    index += 4

    #Left-clicks (int 4 bytes)
    left_clicks = raw_data[index]
    print(f"left_clicks: {left_clicks}")
    res["left_clicks"] = left_clicks
    index += 4

    #Right-clicks (int 4 bytes)
    right_clicks = raw_data[index]
    print(f"right_clicks: {right_clicks}")
    res["right_clicks"] = right_clicks
    index += 4

    #note blocks added (inte 4 bytes)
    note_blocks_added = raw_data[index]
    print(f"note_blocks_added: {note_blocks_added}")
    res["note_blocks_added"] = note_blocks_added
    index += 4

    #note blocks removed (inte 4 bytes)
    note_blocks_removed = raw_data[index]
    print(f"note_blocks_removed: {note_blocks_removed}")
    res["note_blocks_removed"] = note_blocks_removed
    index += 4

    #MIDI/Schematic file name
    midi_or_schematic_file_name, index = read_string(raw_data, index)
    print(f"midi_or_schematic_file_name: {midi_or_schematic_file_name}")
    res["midi_or_schematic_file_name"] = midi_or_schematic_file_name
    index += 1

    #loop_on/off (1 byte)
    loop_on_or_off = raw_data[index]
    print(f"loop_on_or_off: {loop_on_or_off}")
    res["loop_on_or_off"] = loop_on_or_off
    index += 1

    #max_loop_count (1 byte)
    max_loop_count = raw_data[index]
    print(f"max_loop_count: {max_loop_count}")
    res["max_loop_count"] = max_loop_count
    index += 1

    #loop_start_tick (1 byte)
    loop_start_tick = raw_data[index]
    print(f"loop_start_tick: {loop_start_tick}")
    res["loop_start_tick"] = loop_start_tick
    index += 1

    #document index
    res["index"] = index

    return res

#see documentation on .nbs files
def generate_lists (data: bytes, 
                    index: int, 
                    song_tempo: int, 
                    song_length: int) -> list[list[list[int]]]:
    tick = -1
    modulus = song_tempo // 250 #1-8
    song:list[list[list[int]]] = [[[[] for _ in range(25)] for _ in range(modulus)] \
            for _ in range(16)] #instrument -> mod_class -> note -> class_tick

    #0 = Piano (Air)
    #1 = Double Bass (Wood)
    #2 = Bass Drum (Stone)
    #3 = Snare Drum (Sand)
    #4 = Click (Glass)
    #5 = Guitar (Wool)
    #6 = Flute (Clay)
    #7 = Bell (Block of Gold)
    #8 = Chime (Packed Ice)
    #9 = Xylophone (Bone Block)
    #10 = Iron Xylophone (Iron Block)
    #11 = Cow Bell (Soul Sand)
    #12 = Didgeridoo (Pumpkin)
    #13 = Bit (Block of Emerald)
    #14 = Banjo (Hay)
    #15 = Pling (Glowstone)

    while tick < song_length:
        tick += int.from_bytes(data[index:index+2], byteorder='little')
        #print(tick, data[index:index + 12])
        instrument = data[index+4]
        note = data[index+5] - 33
        mod_class = tick % modulus
        class_tick = tick // modulus

        if len(song[instrument][mod_class][note]) == 0 or not song[instrument][mod_class][note][-1] == class_tick:
            song[instrument][mod_class][note].append(class_tick)

        if data[index+8:index+12] == b'\x00\x00\x00\x00':
            index += 12
        else:
            index += 8

    return song

def list_to_unsplit_shulker (li: list[list[list[int]]]) -> list[list[list[int]]]:
    
    res = []
    last_num = 0
    
    for num in li:
        diff = num - last_num

        while diff >= 64:
            res.append(-64)
            diff -= 64
        if diff > 0:
            res.append(diff * -1)
            diff = 0
        if diff == 0:
            res.append(1)

        last_num = num + 1

    return res


def unsplit_shulker_to_split_shulker (li: list[list[list[int]]], res: list[list[list[list[int]]]]) -> list[list[list[list[int]]]]:

    if len(li) <= 27:
        res.append(li)
        return res

    i = 26
    while i >= 0:
        if not li[i] <= -4:
            i -= 1
            continue
        else:
            li[i] += 4
            res.append(li[:i + 1])
            return unsplit_shulker_to_split_shulker(li[i + 1:], res)

    return res


def generate_item_id (li: list[list[list[int]]]) -> str:
    res = '/give @p shulker_box[container=['

    if li[-1] == 0:
        li.pop()

    #item dict
    stackable_items = {
        0: 'white_concrete_powder',
        1: 'light_gray_concrete_powder',
        2: 'gray_concrete_powder',
        3: 'black_concrete_powder',
        4: 'brown_concrete_powder',
        5: 'red_concrete_powder',
        6: 'orange_concrete_powder',
        7: 'yellow_concrete_powder',
        8: 'lime_concrete_powder',
        9: 'green_concrete_powder',
        10: 'cyan_concrete_powder',
        11: 'light_blue_concrete_powder',
        12: 'blue_concrete_powder',
        13: 'purple_concrete_powder',
        14: 'magenta_concrete_powder',
        15: 'pink_concrete_powder',
        16: 'white_concrete',
        17: 'light_gray_concrete',
        18: 'gray_concrete',
        19: 'black_concrete',
        20: 'brown_concrete',
        21: 'red_concrete',
        22: 'orange_concrete',
        23: 'yellow_concrete',
        24: 'lime_concrete',
        25: 'green_concrete',
        26: 'cyan_concrete'
    }

    for i in range(len(li)):
        if li[i] == 1:
            item = 'wooden_shovel'
        else:
            item = stackable_items[i]

        res += f"{{slot:{i},item:{{id:{item},count:{abs(li[i])}}}}}"
        if not i == len(li) - 1:
            res += ','

    res += ']] 1'
    
    return res

def decode(directory: str) -> str:
    res = ''
    with open(directory, 'rb') as file:
        raw_data = file.read()
    header_data = read_header(raw_data)
    nd_array = generate_lists(
        raw_data,
        header_data["index"],
        header_data["song_tempo"],
        header_data["song_length"]
    )
    print('\n')

    for i in range(len(nd_array)):    
        for c in range(len(nd_array[i])):
            for n in range(len(nd_array[i][c])):
                if not nd_array[i][c][n] == []:
                    
                    shulker_li = unsplit_shulker_to_split_shulker(list_to_unsplit_shulker(nd_array[i][c][n]), [])
                    res += f'{i} {c} {n} {shulker_li} \n'
                    #print(i, c, n, shulker_li)

                    if shulker_li == []:
                        res += "WTF \n"
                    elif shulker_li[-1][-1] != 1:
                        res += "WTF WTF \n"

                    num = 1
                    for shulkers in unsplit_shulker_to_split_shulker(list_to_unsplit_shulker(nd_array[i][c][n]), []):
                        res += f'{num} {generate_item_id(shulkers)} \n'
                        #print(num, generate_item_id(shulkers))
                        num += 1

    return res
