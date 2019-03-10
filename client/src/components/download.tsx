import * as React from 'react';

export interface Props {
  pullRight: boolean;
  url: string;
  name: string;
  hideText?: boolean;
}

function Download({url, name, pullRight, hideText}: Props) {
  const download = (
    <span>
      <a
        className="btn btn-sm btn-default"
        href={url}
        download={name}
      >
        <i className="fa fa-cloud-download icon" aria-hidden="true"/> {!hideText && 'Download'}
      </a>
    </span>
  );

  if (pullRight) {
    return (
    <div className="pull-right button-refresh">
      {download}
    </div>
    );
  }
  return download;
}

export default Download;
