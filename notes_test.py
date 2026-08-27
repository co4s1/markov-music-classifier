import random
import copy
import os
import glob
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sns

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


def log_likelyhood(sequence, vocabulary, matrix):
    vocab_lookup = {val: i for i, val in enumerate(vocabulary)}
    log_like = 0
    smallnumber = 1e-10
    for i in range(len(sequence) - 1):
        try:
            curr_idx = vocab_lookup[sequence[i]]
            next_idx = vocab_lookup[sequence[i+1]]
            
            prob = matrix[curr_idx][next_idx]
            if prob <= 0:
                prob = smallnumber
                
            log_like += math.log(prob)
        except KeyError:
            continue 
            
    return log_like


def generate_difference_map(matrix_m, matrix_b, labels, type_label):
    m = np.array(matrix_m, dtype=float)
    b = np.array(matrix_b, dtype=float)
    
    diff = m - b
    
    plt.figure(figsize=(14, 12))
    
    limit = max(abs(diff.min()), abs(diff.max()))
    
    ax = sns.heatmap(diff, 
                     xticklabels=labels if len(labels) < 50 else False, 
                     yticklabels=labels if len(labels) < 50 else False, 
                     cmap='RdBu_r', 
                     center=0,
                     vmin=-limit, 
                     vmax=limit,
                     cbar_kws={'label': 'Mozart dominance (+) vs Bach dominance (-)'})
    
    plt.title(f"Style Differentiation Map: Mozart vs Bach ({type_label})")
    plt.xlabel("Next State")
    plt.ylabel("Current State")
    
    plt.savefig(f"Difference_Map_{type_label}.png", dpi=300, bbox_inches='tight')

if __name__ == "__main__":

    file_pattern = 'test/*.xml'
    file_paths = glob.glob(file_pattern)
    print(file_paths)
    notinmatrix = 0


    test_data = {}
    bach_data = np.load('bach_data.npz')
    mozart_data = np.load('mozart_data.npz')

    bach_note_matrix = bach_data['note_matrix_smooth']
    bach_dur_matrix = bach_data['dur_matrix_smooth']
    bach_c_matrix = bach_data['c_matrix_smooth']

    mozart_note_matrix = mozart_data['note_matrix_smooth']
    mozart_dur_matrix = mozart_data['dur_matrix_smooth']
    mozart_c_matrix = mozart_data['c_matrix_smooth']

    ma = mozart_data['note_labels'].tolist()
    mb = mozart_data['dur_labels'].tolist()
    mc = mozart_data['combined_labels'].tolist()

    ba = bach_data['note_labels'].tolist()
    bb = bach_data['dur_labels'].tolist()
    bc = bach_data['combined_labels'].tolist()
    
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            key_changes = extract_key_changes(lines)
            n, d, c = extract_notes(lines, key_changes)

            test_data[os.path.basename(file_path)] = {
                'notes': n,
                'durs': d,
                'combined': c
            }
  
    print(f"{'File Name':<20} | {'Metric':<10} | {'Mozart LL':<12} | {'Bach LL':<12} | {'Winner'}")
    print("-" * 75)

    for file_path in file_paths:
        fname = os.path.basename(file_path)
        data = test_data[fname]

        results = [
            ("Notes", log_likelyhood(data['notes'], ma, mozart_note_matrix), log_likelyhood(data['notes'], ba, bach_note_matrix)),
            ("Durs",  log_likelyhood(data['durs'], mb, mozart_dur_matrix), log_likelyhood(data['durs'], bb, bach_dur_matrix)),
            ("Comb",  log_likelyhood(data['combined'], mc, mozart_c_matrix), log_likelyhood(data['combined'], bc, bach_c_matrix))
        ]

        for label, m_ll, b_ll in results:
            winner = "Mozart" if m_ll > b_ll else "Bach"
            print(f"{fname[:20]:<20} | {label:<10} | {m_ll:<12.2f} | {b_ll:<12.2f} | {winner}")
        print("-" * 75)

    generate_difference_map(mozart_note_matrix, bach_note_matrix, ma, "note_difference_map")
    generate_difference_map(mozart_c_matrix, bach_c_matrix, mc, "note_and_duration_difference_map")
