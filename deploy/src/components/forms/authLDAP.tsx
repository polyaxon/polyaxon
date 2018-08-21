import * as _ from 'lodash';
import * as React from 'react';

import { AuthInterface, ConfigInterface, LDAPInterface } from '../../interfaces/config';
import PreviewForm from './previewForm';

export interface Props {
  config: ConfigInterface;
  defaultConfig: ConfigInterface;
  updateConfig: (config: ConfigInterface) => void;
}

interface State {
  config: ConfigInterface;
}

export default class AuthLDAP extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      config: this.props.config,
    };
  }

  public updateEnabled = (key: string, value: boolean) => {
    const config = _.cloneDeep(this.state.config);
    if (_.isNil(config.auth)) {
      config.auth = {} as AuthInterface;
    }

    if (_.isNil(config.auth.ldap)) {
      config.auth.ldap = {} as LDAPInterface;
    }

    if (key === 'enabled') {
      if (value) {
        config.auth.ldap.enabled = value;
      } else {
        delete config.auth.ldap;
      }
    } else if (key === 'startTLS') {
      config.auth.ldap.startTLS = value;
    }

    this.setState({config});
  };

  public update = (key: string, value: string) => {
    const config = _.cloneDeep(this.state.config);
    if (_.isNil(config.auth)) {
      config.auth = {} as AuthInterface;
    }

    if (_.isNil(config.auth.ldap)) {
      config.auth.ldap = {} as LDAPInterface;
    }

    if (key === 'serverUri') {
      config.auth.ldap.serverUri = value;
    } else if (key === 'globalOptions') {
      config.auth.ldap.globalOptions = value;
    } else if (key === 'connectionOptions') {
      config.auth.ldap.connectionOptions = value;
    } else if (key === 'bindDN') {
      config.auth.ldap.bindDN = value;
    } else if (key === 'bindPassword') {
      config.auth.ldap.bindPassword = value;
    } else if (key === 'userSearchBaseDN') {
      config.auth.ldap.userSearchBaseDN = value;
    } else if (key === 'userSearchFilterStr') {
      config.auth.ldap.userSearchFilterStr = value;
    } else if (key === 'userDNTemplate') {
      config.auth.ldap.userDNTemplate = value;
    } else if (key === 'connectionOptions') {
      config.auth.ldap.connectionOptions = value;
    } else if (key === 'userAttrMap') {
      config.auth.ldap.userAttrMap = value;
    } else if (key === 'groupSearchBaseDN') {
      config.auth.ldap.groupSearchBaseDN = value;
    } else if (key === 'groupSearchGroupType') {
      config.auth.ldap.groupSearchGroupType = value;
    } else if (key === 'requireGroup') {
      config.auth.ldap.requireGroup = value;
    } else if (key === 'denyGroup') {
      config.auth.ldap.denyGroup = value;
    }

    this.setState({config});
  };

  public componentDidUpdate(prevProps: Props, prevState: State) {
    if (!_.isEqual(this.state.config, prevState.config)) {
      this.props.updateConfig(this.state.config);
    }
  }

  public render() {
    const currentConfig = () => {
      const config: AuthInterface = {};
      if (!_.isNil(this.state.config.auth) && !_.isNil(this.state.config.auth.ldap)) {
        config.ldap = this.state.config.auth.ldap;
      }
      return config;
    };

    const defaultConfig = {
      ldap: this.props.defaultConfig.auth ? this.props.defaultConfig.auth.ldap : {},
    };

    return (
      <div className="columns">
        <div className="column is-7">
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Enable</label>
            </div>
            <div className="field-body">
              <input
                type="checkbox"
                onChange={(event) => this.updateEnabled('enabled', event.target.checked)}
              />
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Server Uri</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={
                      (this.state.config.auth && this.state.config.auth.ldap) ?
                      this.state.config.auth.ldap.serverUri || '' :
                      ''}
                    onChange={(event) => this.update('serverUri', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Global Options</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <textarea
                    className="textarea"
                    rows={2}
                    value={
                      (this.state.config.auth && this.state.config.auth.ldap) ?
                      this.state.config.auth.ldap.globalOptions || '' :
                      ''}
                    onChange={(event) => this.update('globalOptions', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Connection Options</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <textarea
                    className="textarea"
                    rows={2}
                    value={
                      (this.state.config.auth && this.state.config.auth.ldap) ?
                      this.state.config.auth.ldap.connectionOptions || '' :
                      ''}
                    onChange={(event) => this.update('connectionOptions', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Bind DN</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={
                      (this.state.config.auth && this.state.config.auth.ldap) ?
                      this.state.config.auth.ldap.bindDN || '' :
                      ''}
                    onChange={(event) => this.update('bindDN', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Bind Password</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={
                      (this.state.config.auth && this.state.config.auth.ldap) ?
                      this.state.config.auth.ldap.bindPassword || '' :
                      ''}
                    onChange={(event) => this.update('bindPassword', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">User Search Base DN</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={
                      (this.state.config.auth && this.state.config.auth.ldap) ?
                      this.state.config.auth.ldap.userSearchBaseDN || '' :
                      ''}
                    onChange={(event) => this.update('userSearchBaseDN', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">User Search Filter Str</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={
                      (this.state.config.auth && this.state.config.auth.ldap) ?
                      this.state.config.auth.ldap.userSearchFilterStr || '' :
                      ''}
                    onChange={(event) => this.update('userSearchFilterStr', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">User DN Template</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={
                      (this.state.config.auth && this.state.config.auth.ldap) ?
                      this.state.config.auth.ldap.userDNTemplate || '' :
                      ''}
                    onChange={(event) => this.update('userDNTemplate', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Start TLS</label>
            </div>
            <div className="field-body">
              <input
                type="checkbox"
                onChange={(event) => this.updateEnabled('startTLS', event.target.checked)}
              />
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">User Attr Map</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={
                      (this.state.config.auth && this.state.config.auth.ldap) ?
                      this.state.config.auth.ldap.userAttrMap || '' :
                      ''}
                    onChange={(event) => this.update('userAttrMap', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Group Search Base DN</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={
                      (this.state.config.auth && this.state.config.auth.ldap) ?
                      this.state.config.auth.ldap.groupSearchBaseDN || '' :
                      ''}
                    onChange={(event) => this.update('groupSearchBaseDN', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Group Search Group Type</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={
                      (this.state.config.auth && this.state.config.auth.ldap) ?
                      this.state.config.auth.ldap.groupSearchGroupType || '' :
                      ''}
                    onChange={(event) => this.update('groupSearchGroupType', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Require Group</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={
                      (this.state.config.auth && this.state.config.auth.ldap) ?
                      this.state.config.auth.ldap.requireGroup || '' :
                      ''}
                    onChange={(event) => this.update('requireGroup', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Deny Group</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={
                      (this.state.config.auth && this.state.config.auth.ldap) ?
                      this.state.config.auth.ldap.denyGroup || '' :
                      ''}
                    onChange={(event) => this.update('denyGroup', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        <PreviewForm currentConfig={currentConfig()} defaultConfig={defaultConfig}/>
      </div>
    );
  }
}
