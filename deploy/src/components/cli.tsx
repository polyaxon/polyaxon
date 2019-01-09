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
  };

  public useVirtualenv = (value: boolean) => {
    this.setState({useVirtualenv: value});
  };

  public render() {
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
                        className={'button ' + (this.state.os === 'macOS' ? 'is-info is-active' : '')}
                        onClick={() => this.setKey('os', 'macOS')}
                      >
                        macOS
                      </a>
                    </p>
                    <p className="control">
                      <a
                        className={'button ' + (this.state.os === 'Windows' ? 'is-info is-active' : '')}
                        onClick={() => this.setKey('os', 'Windows')}
                      >
                        Windows
                      </a>
                    </p>
                    <p className="control">
                      <a
                        className={'button ' + (this.state.os === 'Linux' ? 'is-info is-active' : '')}
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
                        className={'button ' + (this.state.install === 'pip' ? 'is-info is-active' : '')}
                        onClick={() => this.setKey('install', 'pip')}
                      >
                        With pip
                      </a>
                    </p>
                    <p className="control">
                      <a
                        className={'button ' + (this.state.install === 'source' ? 'is-info is-active' : '')}
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
                        className={'button ' + (this.state.pythonVersion === '2.x' ? 'is-info is-active' : '')}
                        onClick={() => this.setKey('pythonVersion', '2.x')}
                      >
                        2.x
                      </a>
                    </p>
                    <p className="control">
                      <a
                        className={'button ' + (this.state.pythonVersion === '3.x' ? 'is-info is-active' : '')}
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
            <pre className="content content-output code">
              {this.state.useVirtualenv && this.state.pythonVersion === '2.x' &&
              <code>
                  <span className="bash">
                    python -m pip install -U virtualenv
                  </span>
                <span className="bash">
                    virtualenv .python-env
                  </span>
                {this.state.os === 'Windows' ?
                  <span className="bash">
                    .env\Scripts\activate
                  </span> :
                  <span className="bash">
                    source .env/bin/activate
                  </span>
                }
              </code>
              }
              {this.state.useVirtualenv && this.state.pythonVersion === '3.x' &&
              <code>
                <span className="bash">
                  python -m pip install -U venv
                </span>
                <span className="bash">
                  python -m venv .env
                </span>
                {this.state.os === 'Windows' ?
                  <span className="bash">
                    .env\Scripts\activate
                  </span> :
                  <span className="bash">
                    source .env/bin/activate
                  </span>
                }
              </code>
              }
              {this.state.install === 'pip' &&
              <code>
                <span className="bash">
                  pip install -U polyaxon-cli
                </span>
              </code>
              }
              {this.state.install === 'source' &&
              <code>
                <span className="bash">
                  git clone https://github.com/polyaxon/polyaxon-cli
                </span>
                <span className="bash">
                  cd polyaxon-cli
                </span>
                <span className="bash">
                  python setup.py install
                </span>
              </code>
              }
            </pre>
          </figure>
        </div>
      </div>
    );

  }
}
