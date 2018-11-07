import * as _ from 'lodash';
import * as React from 'react';

import { decorators, Treebeard } from 'react-treebeard';
import * as actions from '../../actions/outputs';
import { CODE_EXTENSIONS, IMAGE_EXTENSIONS, TEXT_EXTENSIONS } from '../../constants/extensions';
import { OutputsNode, TreeNode } from '../../models/outputs';
import Refresh from '../refresh';
import OutputsImg from './outputsImg';
import OutputsTxt from './outputsTxt';
import { OUTPUTS_TREE_STYLE } from './treeViewStyle';

import './outputs.less';

export interface Props {
  outputsTree: { [key: string]: OutputsNode };
  outputsFiles: { [key: string]: string };
  fetchOutputsTree: (path: string) => actions.OutputsAction;
  fetchOutputsFiles: (path: string, filetype: string) => actions.OutputsAction;
}

export interface State {
  activeNodeId?: string;
  toggledNodeIds: { [key: string]: boolean };
  requestedNodeIds: Set<string>;
  outputsTree: { [key: string]: OutputsNode };
  outputsFiles: { [key: string]: string };
}

export default class Outputs extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      outputsTree: this.props.outputsTree,
      outputsFiles: this.props.outputsFiles,
      requestedNodeIds: new Set(),
      activeNodeId: undefined,
      toggledNodeIds: {},
    };
  }

  public componentDidMount() {
    this.props.fetchOutputsTree('');
  }

  public componentDidUpdate(prevProps: Props, prevState: State) {
    if (!_.isEqual(this.props.outputsTree, prevProps.outputsTree) ||
      !_.isEqual(this.props.outputsFiles, prevProps.outputsFiles)) {
      this.setState({
        ...prevState,
        outputsTree: this.props.outputsTree,
        outputsFiles: this.props.outputsFiles,
      });
    }
  }

  public refresh = () => {
    this.props.fetchOutputsTree('');
  };

  public onToggle = (node: any, toggled: any) => {
    if (node.loading && !this.state.requestedNodeIds.has(node.id)) {
      this.props.fetchOutputsTree(node.id);
    }
    const child = OutputsNode.findChild(this.state.outputsTree.root, node.id);
    if (_.isNil(this.state.outputsFiles[node.id]) && !child.isDir) {
      const extension = this.getExtension(node.id);
      if (this.isImage(extension)) {
        this.props.fetchOutputsFiles(node.id, 'img');
      } else if (this.isCode(extension) || this.isText(extension)) {
        this.props.fetchOutputsFiles(node.id, 'txt');
      }
    }
    this.setState((prevState, prevProps) => ({
      ...prevState,
      ...{
        activeNodeId: node.id,
        toggledNodeIds: {
          ...this.state.toggledNodeIds,
          [node.id]: toggled,
        },
      }
    }));
  };

  public getData = (parentPath: string, outputsNode: OutputsNode): TreeNode => {
    if (outputsNode.isRoot) {
      if (outputsNode.children) {
        const nodes: TreeNode[] = [];
        for (const nodeName of Object.keys(outputsNode.children)) {
          nodes.push(this.getData(outputsNode.path, outputsNode.children[nodeName]));
        }
        return {children: nodes} as TreeNode;
      }
      // This case should never happen since we should never call this function on an empty root.
      throw Error('unreachable code.');
    }

    const id = parentPath ? `${parentPath}/${outputsNode.path}` : outputsNode.path;
    const name = outputsNode.path;
    let toggled;
    let children;
    let active;

    const toggleState = this.state.toggledNodeIds[id];
    if (toggleState) {
      toggled = toggleState;
    }

    if (outputsNode.children) {
      children = [];
      for (const nodeName of Object.keys(outputsNode.children)) {
        children.push(this.getData(outputsNode.path, outputsNode.children[nodeName]));
      }
    }

    if (this.state.activeNodeId === id) {
      active = true;
    }

    const loading = outputsNode.children !== undefined && !outputsNode.isLoaded;

    return {
      id,
      name,
      toggled,
      children,
      active,
      loading,
    } as TreeNode;
  };

  public getExtension = (path: string) => {
    const parts = path.split(/[./]/);
    return parts[parts.length - 1];
  };

  public isImage = (extension: string) => {
    return IMAGE_EXTENSIONS.has(extension);
  };

  public isCode = (extension: string) => {
    return CODE_EXTENSIONS.has(extension);
  };

  public isText = (extension: string) => {
    return TEXT_EXTENSIONS.has(extension);
  };

  public render() {
    const nodeHeader = (props: any) => {
      let iconType;
      if (props.node.children) {
        iconType = 'folder';
      } else {
        const extension = this.getExtension(props.node.name);
        if (this.isImage(extension)) {
          iconType = 'file-image-o';
        } else if (this.isCode(extension)) {
          iconType = 'file-code-o';
        } else if (this.isText(extension)) {
          iconType = 'file-text-o';
        } else {
          iconType = 'file';
        }
      }
      const iconClass = `fa fa-${iconType}`;

      return (
        <div style={props.style.base}>
          <div style={props.style.title}>
            <i className={iconClass}/> {props.node.name}
          </div>
        </div>
      );
    };

    const nodeLoading = (props: any) => {
      return (
        <div style={props.style}>
          <i className="fa fa-refresh"/> loading...
        </div>
      );
    };

    const getFileHeader = () => {
      if (!this.state.activeNodeId) {
        return (null);
      }
      const node = OutputsNode.findChild(this.state.outputsTree.root, this.state.activeNodeId);
      return (
        <div className="row">
          <div className="col-md-12">
            <div className="file-header">
              <p>Type: {node.isDir ? 'directory' : 'file'}</p>
              <p>Path: {this.state.activeNodeId}</p>
              {!node.isDir && <p>Size: {node.size}</p>}
            </div>
          </div>
        </div>
      );
    };

    const getFile = () => {
      if (this.state.activeNodeId &&
        !OutputsNode.findChild(this.state.outputsTree.root, this.state.activeNodeId).isDir) {
        if (this.state.outputsFiles[this.state.activeNodeId]) {
          const extension = this.getExtension(this.state.activeNodeId);
          if (this.isCode(extension) || this.isText(extension)) {
            return (
              <OutputsTxt
                key={this.state.activeNodeId}
                outputsFile={this.state.outputsFiles[this.state.activeNodeId]}
              />
            );
          } else if (this.isImage(extension)) {
            return (<OutputsImg outputsFile={this.state.outputsFiles[this.state.activeNodeId]}/>);
          }
        } else {
          return (
            <div className="row">
              <div className="col-md-offset-2 col-md-8">
                <div className="jumbotron jumbotron-action text-center empty-jumbotron">
                  <h3>This extension is not supported.</h3>
                  <div>Only text files and images can be previewed.</div>
                </div>
              </div>
            </div>
          );
        }
      }
      return (null);
    };

    decorators.Header = nodeHeader;
    decorators.Loading = nodeLoading;
    return (
      <div className="outputs">
        <div className="row">
          <div className="col-md-12 button-refresh-alone">
            <Refresh callback={this.refresh} pullRight={true}/>
          </div>
        </div>
        <div className="row">
          <div className="col-md-12">
            <div className="outputs-header">
              Outputs
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col-md-4">
            {this.state.outputsTree.root
              ? <Treebeard
                data={this.getData('', this.state.outputsTree.root).children}
                onToggle={this.onToggle}
                style={OUTPUTS_TREE_STYLE}
                decorators={decorators}
              />
              : ''
            }
          </div>
          <div className="col-md-8">
            {getFileHeader()}
            {getFile()}
          </div>
        </div>
      </div>
    );
  }
}
