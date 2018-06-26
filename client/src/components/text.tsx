import * as React from 'react';

import './text.less';

export interface Props {
  title: string;
  text: string;
}

function Text({text, title}: Props) {
  let processedText = (text && text.length > 0) ?
    text.split('\n').map((line, i) => <p key={i}>{line}</p>) :
    <p>No content!</p>;
  function getText() {
    return (
      <div className="text">
        <div className="row">
          <div className="col-md-12">
            <div className="text-header">
              {title}
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col-md-12">
            <div className="text-content">
              {processedText}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (getText());
}

export default Text;
