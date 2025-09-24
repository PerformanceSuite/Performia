import React from 'react';
import { produce } from 'immer';
import { SongMap } from '../types';

interface BlueprintViewProps {
    songMap: SongMap;
    onSongMapChange: (newSongMap: SongMap) => void;
}

const BlueprintView: React.FC<BlueprintViewProps> = ({ songMap, onSongMapChange }) => {

    const handleBlur = (e: React.FocusEvent<HTMLElement>, updateFn: (draft: SongMap) => void) => {
        const newSongMap = produce(songMap, updateFn);
        onSongMapChange(newSongMap);
    };

    return (
        <div className="blueprint-view flex-grow overflow-y-auto">
            <div className="max-w-4xl mx-auto">
                <div className="blueprint-header">
                    <h1 
                        contentEditable 
                        suppressContentEditableWarning 
                        onBlur={(e) => handleBlur(e, draft => { draft.title = e.currentTarget.textContent || ''; })}
                    >
                        {songMap.title}
                    </h1>
                    <h2 
                        contentEditable 
                        suppressContentEditableWarning
                        onBlur={(e) => handleBlur(e, draft => { draft.artist = e.currentTarget.textContent || ''; })}
                    >
                        {songMap.artist}
                    </h2>
                </div>

                {songMap.sections.map((section, sectionIndex) => (
                    <div key={sectionIndex}>
                        <h3 
                            className="blueprint-section-header"
                            contentEditable
                            suppressContentEditableWarning
                            onBlur={(e) => handleBlur(e, draft => { 
                                draft.sections[sectionIndex].name = (e.currentTarget.textContent || '').replace(/[\[\]\s]/g, ''); 
                            })}
                        >
                            [ {section.name} ]
                        </h3>
                        {section.lines.map((line, lineIndex) => (
                            <div key={lineIndex} className="blueprint-line">
                                {line.syllables.map((syllable, syllableIndex) => (
                                    <div key={syllableIndex} className="blueprint-syllable">
                                        <span 
                                            className="chord"
                                            contentEditable
                                            suppressContentEditableWarning
                                            onBlur={(e) => handleBlur(e, draft => {
                                                draft.sections[sectionIndex].lines[lineIndex].syllables[syllableIndex].chord = e.currentTarget.textContent || undefined;
                                            })}
                                        >
                                            {syllable.chord || ''}
                                        </span>
                                        <span 
                                            className="lyric"
                                            contentEditable
                                            suppressContentEditableWarning
                                            onBlur={(e) => handleBlur(e, draft => {
                                                draft.sections[sectionIndex].lines[lineIndex].syllables[syllableIndex].text = e.currentTarget.textContent || '';
                                            })}
                                        >
                                            {syllable.text}
                                        </span>
                                    </div>
                                ))}
                            </div>
                        ))}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default BlueprintView;
