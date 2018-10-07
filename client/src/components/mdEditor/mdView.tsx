import * as React from 'react';

import * as Showdown from 'showdown';

import { getConverter, sanitizeHtml } from '../../utils/md';

import './md.less';

interface Props {
  content: string;
  onEdit: () => void;
}

export default class MDView extends React.Component<Props, {}> {
  public converter: Showdown.Converter;

  constructor(props: Props) {
    super(props);
    this.converter = getConverter();
  }

  public render() {
    const html = sanitizeHtml(this.converter.makeHtml(this.props.content || ''));
    return (
      <div className="row">
        <div className="col-md-12">

          <div className="md-header">
            <div className="row">
              <div className="col-md-11 block">
                <i className="fa fa-book icon" aria-hidden="true"/> Readme
              </div>
              <div className="col-md-1 block">
                <span className="md-edit" onClick={() => this.props.onEdit()}>
                  <i className="fa fa-pencil icon pull-right" aria-hidden="true"/>
                </span>
              </div>
            </div>
          </div>

          <div className="row">
            <div className="col-md-12">
              <div className="md-view">
                <div
                  dangerouslySetInnerHTML={{__html: html || '<p>&nbsp;</p>'}}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
