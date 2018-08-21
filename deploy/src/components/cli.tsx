import * as React from 'react';

export interface CliState {
  os: string;
  install: string;
  pythonVersion: string;
  useVirtualenv: boolean;
}

export default class Cli extends React.Component<{}, CliState> {

  constructor(props: any) {
    super(props);
    this.state = {
      os: 'macOS',
      install: 'pip',
      pythonVersion: '3.x',
      useVirtualenv: false,
    };
  }

  public setKey = (key: string, value: string) => {
    if (key === 'os') {
      this.setState({os: value});
    } else if (key === 'install') {
      this.setState({install: value});
    } else if (key === 'pythonVersion') {
      this.setState({pythonVersion: value});
    }
  }

  public useVirtualenv = (value: boolean) => {
    this.setState({useVirtualenv: value});
  };

  public render() {
    const command = () => {
      if (this.state.install === 'pip') {
        return 'pip install -U polyaxon-cli';
      }
      return '';
    }
    return (
      <div className="columns">
        <div className="column is-7">
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">OS</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <div className="field is-grouped">
                    <p className="control">
                      <a
                        className={'button ' + (this.state.os === 'macOS' ? 'is-link is-active' : '')}
                        onClick={() => this.setKey('os', 'macOS')}
                      >
                        macOS
                      </a>
                    </p>
                    <p className="control">
                      <a
                        className={'button ' + (this.state.os === 'Windows' ? 'is-link is-active' : '')}
                        onClick={() => this.setKey('os', 'Windows')}
                      >
                        Windows
                      </a>
                    </p>
                    <p className="control">
                      <a
                        className={'button ' + (this.state.os === 'Linux' ? 'is-link is-active' : '')}
                        onClick={() => this.setKey('os', 'Linux')}
                      >
                        Linux
                      </a>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Install</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <div className="field is-grouped">
                    <p className="control">
                      <a
                        className={'button ' + (this.state.install === 'pip' ? 'is-link is-active' : '')}
                        onClick={() => this.setKey('install', 'pip')}
                      >
                        With pip
                      </a>
                    </p>
                    <p className="control">
                      <a
                        className={'button ' + (this.state.install === 'source' ? 'is-link is-active' : '')}
                        onClick={() => this.setKey('install', 'source')}
                      >
                        From source
                      </a>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Python version</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <div className="field is-grouped">
                    <p className="control">
                      <a
                        className={'button ' + (this.state.pythonVersion === '2.x' ? 'is-link is-active' : '')}
                        onClick={() => this.setKey('pythonVersion', '2.x')}
                      >
                        2.x
                      </a>
                    </p>
                    <p className="control">
                      <a
                        className={'button ' + (this.state.pythonVersion === '3.x' ? 'is-link is-active' : '')}
                        onClick={() => this.setKey('pythonVersion', '3.x')}
                      >
                        3.x
                      </a>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Use virtualenv</label>
            </div>
            <div className="field-body">
              <input
                type="checkbox"
                onChange={(event) => this.useVirtualenv(event.target.checked)}
              />
            </div>
          </div>
        </div>
        <div className="column is-5 preview">
          <figure className="content-figure">
                <pre className="content content-output">
                  <p>
                     fooo
                  </p>
                </pre>
          </figure>
        </div>
      </div>
    );

  }
}
