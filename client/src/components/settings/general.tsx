import * as React from 'react';

import * as actions from '../../actions/options';
import Option from '../../containers/options/option';
import { OptionModel } from '../../models/option';
import SettingsSidebar from './sidebar';

import './settings.less';

export interface Props {
  section: string;
  options: OptionModel[];
  onFetch: () => actions.OptionAction;
}

export default class GeneralSettings extends React.Component<Props, {}> {
  public componentDidMount() {
    this.props.onFetch();
  }

  public render() {
    return (
      <div className="row settings">
        <div className="col-md-3">
          <SettingsSidebar/>
        </div>
        <div className="col-md-9">
          <h3 className="menu-header">{this.props.section}</h3>
          {this.props.options.map((option: OptionModel) => <Option key={option.key} option={option} />)}
        </div>
      </div>
    );
  }
}
