import random
import copy
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

note_map = {
    'C': 0,   'C#': 1,  'C##': 2,  'Cb': 11, 'Cbb': 10,
    'D': 2,   'D#': 3,  'D##': 4,  'Db': 1,  'Dbb': 0,
    'E': 4,   'E#': 5,  'E##': 6,  'Eb': 3,  'Ebb': 2,
    'F': 5,   'F#': 6,  'F##': 7,  'Fb': 4,  'Fbb': 3,
    'G': 7,   'G#': 8,  'G##': 9,  'Gb': 6,  'Gbb': 5,
    'A': 9,   'A#': 10, 'A##': 11, 'Ab': 8,  'Abb': 7,
    'B': 11,  'B#': 0,  'B##': 1,  'Bb': 10, 'Bbb': 9
}

midi_map = {
    0: 'C',
    1: 'C#',
    2: 'D',
    3: 'D#',
    4: 'E',
    5: 'F',
    6: 'F#',
    7: 'G',
    8: 'G#',
    9: 'A',
    10: 'A#',
    11: 'B'
}

fifths_to_transpose = {
    -7: 11,
    -6: 6,
    -5: 1,
    -4: 8,
    -3: 3,
    -2: 10,
    -1: 5,
    0: 0,
    1: 7,
    2: 2,
    3: 9,
    4: 4, 
    5: 11,
    6: 6, 
    7: 1
}
def extract_key_changes(lines):
    key_changes = []
    
    for i, line in enumerate(lines):
        if '<key>' in str(line):
            for j in range(i, min(i+10, len(lines))):
                if '<fifths>' in str(lines[j]):
                    fifths_line = lines[j].strip()
                    start = fifths_line.find('<fifths>') + 8
                    end = fifths_line.find('</fifths>')
                    fifths = int(fifths_line[start:end])
                    transpose_semitones = fifths_to_transpose[fifths]
                    key_changes.append({'line': i, 'fifths': fifths, 'transpose': transpose_semitones})
                    break
    
    return key_changes

def generate_matrix_image(matrix, labels, composer_name, type_label):
    plot_data = np.array(matrix, dtype=float)
    plot_data = np.log1p(plot_data) 
    plt.figure(figsize=(12, 10))
    if type_label == 'Notes' or type_label == "Durations":
        ax = sns.heatmap(plot_data, 
                     xticklabels=labels, 
                     yticklabels=labels, 
                     cmap='magma', 
                     cbar_kws={'label': 'Log-scaled Probability'})
    else:
        ax = sns.heatmap(plot_data, 
                     xticklabels=False, 
                     yticklabels=False, 
                     cmap='magma', 
                     cbar_kws={'label': 'Log-scaled Probability'})
    
    plt.title(f"Musical DNA Map: {composer_name} ({type_label})")
    plt.xlabel("Next Note (MIDI)")
    plt.ylabel("Current Note (MIDI)")
    
    plt.savefig(f"maps/{composer_name}_{type_label}_dna.png", dpi=300, bbox_inches='tight')



def extract_notes(lines, key_changes):
    current_transpose = 0
    key_change_idx = 0
    current_divisions = 1

    extracted_notes = []
    extreacted_dur = []
    comb_notesanddur = []

    for i, line in enumerate(lines):
        if '<divisions>' in line:
            start = line.find('<divisions>') + 11
            end = line.find('</divisions>')
            current_divisions = int(line[start:end])

        if key_change_idx < len(key_changes) and i >= key_changes[key_change_idx]['line']:
            current_transpose = key_changes[key_change_idx]['transpose']
            key_change_idx += 1
        
        if str(line).strip().startswith('<note'):
            noteblock = []
            j = 0
            while str(lines[i+j]).strip() != '</note>':
                noteblock.append(lines[i+j].strip())
                j += 1
                if str(lines[i+j]).strip() == '</note>':
                    break
            
            if any(bnote.startswith('<rest') for bnote in noteblock) != 1:
                if any(bnote.startswith('<staff>2') for bnote in noteblock) != 1:
                    idx_step = next((index for index, item in enumerate(noteblock) if item.startswith('<step')), None)
                    idx_octave = next((index for index, item in enumerate(noteblock) if item.startswith('<octave')), None)
                    idx_alter = next((index for index, item in enumerate(noteblock) if item.startswith('<alter')), None)
                    idx_dur = next((index for index, item in enumerate(noteblock) if item.startswith('<dur')), None)
                    if idx_step != None and idx_octave != None and idx_dur != None:
                        step = noteblock[idx_step][6:7]
                        octave = int(noteblock[idx_octave][8:9])
                        alter = None

                        dur_raw = int(noteblock[idx_dur][10:].split('<')[0])
                        beat_duration = (dur_raw / current_divisions)
                
                        extreacted_dur.append(beat_duration)
                        
                        if idx_alter != None:
                            if noteblock[idx_alter][7:8] == '1': alter = '#'
                            elif noteblock[idx_alter][7:8] == '2': alter = '##'
                            elif noteblock[idx_alter][7:8] == '-': alter = 'b'
                            elif noteblock[idx_alter][7:8] == '-2': alter = 'bb'
                            else: alter = ''
                            note = str(step) + str(alter)
                        else:
                            note = str(step)
                        
                        midi_note = ((octave + 1) * 12) + note_map[note]
                        transposed_midi = midi_note - current_transpose
                        
                        extracted_notes.append(str(transposed_midi))
                        comb_notesanddur.append(str(transposed_midi) + str(beat_duration))

    return extracted_notes, extreacted_dur, comb_notesanddur

def iterate_pairs(sequence, vocabulary, matrix):
    for i in range(len(sequence) - 1):
        idx_curr = vocabulary.index(sequence[i])
        idx_next = vocabulary.index(sequence[i+1])
        if matrix[idx_curr][idx_next] != None:
            matrix[idx_curr][idx_next] += 1
        else:
            matrix[idx_curr][idx_next] = 1

    j = 0
    while j < len(matrix):
        row_sum = sum(val for val in matrix[j] if val is not None)
        if row_sum > 0:
            k = 0
            while k < len(matrix[j]):
                if matrix[j][k] is not None:
                    matrix[j][k] = matrix[j][k] / row_sum
                else:
                    matrix[j][k] = 0
                k += 1
        j += 1
    return matrix

def iterate_pairs_smooth(sequence, vocabulary, matrix):
    for i in range(len(sequence) - 1):
        idx_curr = vocabulary.index(sequence[i])
        idx_next = vocabulary.index(sequence[i+1])
        if matrix[idx_curr][idx_next] != None:
            matrix[idx_curr][idx_next] += 1
        else:
            matrix[idx_curr][idx_next] = 1

    j = 0
    while j < len(matrix):
        row_sum = sum(val for val in matrix[j] if val is not None)
        if row_sum > 0:
            k = 0
            while k < len(matrix[j]):
                if matrix[j][k] is not None:
                    matrix[j][k] = matrix[j][k] / row_sum
                else:
                    matrix[j][k] = 0
                k += 1
        j += 1
    return matrix
        

def calculate_distribution(sequence, vocabulary, distribution):
    for i in range(len(sequence)):
        idx = vocabulary.index(sequence[i])
        if distribution[idx] != None:
            distribution[idx] += 1
        else:
            distribution[idx] = 1
    
    row_sum = sum(val for val in distribution if val is not None)
    j = 0
    while j < len(distribution):
        if distribution[j] != None:
            distribution[j] = distribution[j] / row_sum
        else:
            distribution[j] = 0
        j += 1
    return distribution


def matrix_to_matrixrange(m):
    matrixrange = copy.deepcopy(m)
    i = 0
    j = 0
    while i < (len(matrixrange)):
        while j < (len(matrixrange) - 1):
            if m[i][j+1] != None:
                matrixrange[i][j+1] = matrixrange[i][j] + m[i][j+1]
            else:
                matrixrange[i][j+1] = matrixrange[i][j]
            j+=1
        i+=1
        j=0
    return(matrixrange)

def generate_from_markov(vocabulary, matrix_range, distribution, length):
    generated_output = []
    dist_ranges = distribution[:]
    
    for j in range(len(dist_ranges) - 1):
        dist_ranges[j+1] = dist_ranges[j] + distribution[j+1]

    first_seed = random.random()
    for k in range(len(dist_ranges)):
        if first_seed < dist_ranges[k]:
            generated_output.append(vocabulary[k])
            break

    i = 0
    while i < length:
        previous_item = generated_output[-1]
        seed = random.random()
        row_idx = vocabulary.index(previous_item)
        for l in range(len(matrix_range[row_idx])):
            if seed < matrix_range[row_idx][l]:
                generated_output.append(vocabulary[l])
                break
        i += 1
    return generated_output

def unmidi(mel, r):
    normalmel = []
    for i in mel:
        midi_num = int(i)
        octave = (midi_num // 12) - 1
        note_in_octave = midi_num % 12
        note_name = midi_map[note_in_octave]
        normalmel.append(note_name + str(octave))
    return normalmel


if __name__ == "__main__":
    composer = 'bach'
    smoothing = 1
    mozart_file_pattern = 'mozart/*.xml'
    bach_file_pattern = 'bach/*.xml'
    mozart_file_paths = glob.glob(mozart_file_pattern)
    bach_file_paths = glob.glob(bach_file_pattern)
    
    all_mozart_notes = []
    all_mozart_durs = []
    all_mozart_combined = []
    
    all_bach_notes = []
    all_bach_durs = []
    all_bach_combined = []
    
    for mozart_file_path in mozart_file_paths:
        with open(mozart_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            key_changes = extract_key_changes(lines)
            notes, durs, comb = extract_notes(lines, key_changes)
            all_mozart_notes.extend(notes)
            all_mozart_durs.extend(durs)
            all_mozart_combined.extend(comb)
    
    for bach_file_path in bach_file_paths:
        with open(bach_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            key_changes = extract_key_changes(lines)
            notes, durs, comb = extract_notes(lines, key_changes)
            all_bach_notes.extend(notes)
            all_bach_durs.extend(durs)
            all_bach_combined.extend(comb)
    
    a = sorted(list(set(all_mozart_notes + all_bach_notes)))
    b = sorted(list(set(all_mozart_durs + all_bach_durs)))
    c = sorted(list(set(all_mozart_combined + all_bach_combined)))
    
    print(f"Notes: {len(a)}")
    print(f"Durations: {len(b)}")
    print(f"Combined: {len(c)}")
    
    
    if composer == 'mozart':
        train_notes = all_mozart_notes
        train_durs = all_mozart_durs
        train_combined = all_mozart_combined
    else:
        train_notes = all_bach_notes
        train_durs = all_bach_durs
        train_combined = all_bach_combined

    note_matrix = [[0.0] * len(a) for _ in range(len(a))]
    dur_matrix = [[0.0] * len(b) for _ in range(len(b))]
    c_matrix = [[0.0] * len(c) for _ in range(len(c))]
    
    note_matrix_smooth = [[smoothing] * len(a) for _ in range(len(a))]
    dur_matrix_smooth = [[smoothing] * len(b) for _ in range(len(b))]
    c_matrix_smooth = [[smoothing] * len(c) for _ in range(len(c))]

    note_matrix_smooth = iterate_pairs_smooth(train_notes, a, note_matrix)
    dur_matrix_smooth = iterate_pairs_smooth(train_durs, b, dur_matrix)
    c_matrix_smooth = iterate_pairs_smooth(train_combined, c, c_matrix)

    note_matrix_smooth = iterate_pairs_smooth(train_notes, a, note_matrix_smooth)
    dur_matrix_smooth = iterate_pairs_smooth(train_durs, b, dur_matrix_smooth)
    c_matrix_smooth = iterate_pairs_smooth(train_combined, c, c_matrix_smooth)
    
    note_distribution = [0.0] * len(a)
    dur_distribution = [0.0] * len(b)
    c_distribution = [0.0] * len(c)
    
    note_distribution = calculate_distribution(train_notes, a, note_distribution)
    dur_distribution = calculate_distribution(train_durs, b, dur_distribution)
    c_distribution = calculate_distribution(train_combined, c, c_distribution)
    
    output_filename = f"{composer}_data.npz"
    np.savez(output_filename, 
             note_matrix_smooth=np.array(note_matrix_smooth, dtype=float),
             dur_matrix_smooth=np.array(dur_matrix_smooth, dtype=float),
             c_matrix_smooth=np.array(c_matrix_smooth, dtype=float),
             note_labels=np.array(a),
             dur_labels=np.array(b),
             combined_labels=np.array(c),
             note_dist=np.array(note_distribution, dtype=float),
             dur_dist=np.array(dur_distribution, dtype=float))
    
    generate_matrix_image(note_matrix_smooth, a, composer, "notes_smooth")
    generate_matrix_image(dur_matrix_smooth, b, composer, "durations_smooth")
    generate_matrix_image(c_matrix_smooth, c, composer, "notes_and_durations_smooth")

    generate_matrix_image(note_matrix, a, composer, "notes")
    generate_matrix_image(dur_matrix, b, composer, "durations")
    generate_matrix_image(c_matrix, c, composer, "notes_and_durations")

    
    print(len(train_notes))
