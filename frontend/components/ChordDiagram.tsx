import React from 'react';
import { chordSVGs } from '../data/chordDiagramsData';

interface ChordDiagramProps {
    chordName: string;
}

const ChordDiagram: React.FC<ChordDiagramProps> = ({ chordName }) => {
    const svgString = chordSVGs[chordName];

    if (!svgString) {
        return <span className="text-xs text-gray-500">N/A</span>;
    }

    return (
        <div dangerouslySetInnerHTML={{ __html: svgString }} />
    );
};

export default ChordDiagram;
