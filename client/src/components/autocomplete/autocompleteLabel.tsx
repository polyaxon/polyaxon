import * as React from 'react';

import './autocompleteLabel.less';

interface AutocompleteLabelProps {
  value: string;
  onClick: (value: string, type?: string) => any;
  type?: string;
}

export default function AutocompleteLabel({value, onClick, type}: AutocompleteLabelProps) {
  return (
    <span className="autocomplete-label-container">
      {type &&
      <span className="label autocomplete-label">{type}:</span>
      }
      <span className="label autocomplete-label autocomplete-label-value">
        <span>{value}</span>
        <span className="remove" onClick={() => onClick(value, type)}>
          <i className="fas fa-times icon" aria-hidden="true"/>
        </span>
      </span>
    </span>
  );
}
