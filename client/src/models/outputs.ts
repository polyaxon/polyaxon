export interface TreeNode {
  id: string;
  name: string;
  toggled: boolean;
  children: TreeNode[];
  active: boolean;
  loading: boolean;
}

export class OutputsNode {
  public isRoot: boolean;
  public isLoaded: boolean;
  public path: string;
  public isDir: boolean;
  public size: string;
  public children?: { [key: string]: OutputsNode };

  public static findChild(node: OutputsNode, path: string) {
    const parts = path.split('/');
    let currentNode = node;
    let resultNode: OutputsNode | null = null;
    parts.forEach((part) => {
      if (currentNode.children && currentNode.children[part] !== undefined) {
        resultNode = currentNode.children[part];
        currentNode = currentNode.children[part];
      } else {
        resultNode = null;
      }
    });
    return resultNode;
  }

  public static isEmpty(node: OutputsNode) {
    return node.children === undefined || Object.keys(node.children).length === 0;
  }

  constructor(isRoot: boolean,
              path: string,
              isDir: boolean,
              size: string,
              children?: { [key: string]: any }) {
    this.isRoot = isRoot;
    this.isLoaded = false;
    this.path = path;
    this.isDir = isDir;
    this.size = size;
    this.children = children;
  }

  public deepCopy() {
    const node = new OutputsNode(this.isRoot, this.path, this.isDir, this.size, undefined);
    node.isLoaded = this.isLoaded;
    if (this.children) {
      const copiedChildren: { [key: string]: OutputsNode } = {};
      for (const name of Object.keys(this.children)) {
        copiedChildren[name] = this.children[name].deepCopy();
      }
      node.children = copiedChildren;
    }
    return node;
  }

  public setChildren(path: string, files: string[][], dirs: string[]) {
    this.isLoaded = true;

    if (files) {
      const newChildren: { [key: string]: OutputsNode } = {};
      files.forEach((fileInfo: string[]) => {
        newChildren[fileInfo[0]] = new OutputsNode(false, fileInfo[0], false, fileInfo[1]);
      });
      dirs.forEach((dir: string) => {
        newChildren[dir] = new OutputsNode(false, dir, true, '', {});
      });
      this.children = newChildren;
    }
  }
}

export class OutputsModel {
  public outputsTree: { [key: string]: OutputsNode };
  public outputsFiles: { [key: string]: string };
}

export const OutputsEmptyState = {
  outputsTree: {},
  outputsFiles: {},
};
