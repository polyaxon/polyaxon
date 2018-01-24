import * as React from "react";
import * as _ from "lodash";

import Group from "./group";
import {GroupModel} from "../models/group";


export interface Props {
  groups: GroupModel[];
  onCreate: (group: GroupModel) => any;
  onUpdate: (group: GroupModel) => any;
  onDelete: (group: GroupModel) => any;
  fetchData: () => any
}


export default class Groups extends React.Component<Props, Object> {
  componentDidMount() {
    const {groups, onCreate, onUpdate, onDelete, fetchData} = this.props;
    fetchData();
  }

  public render() {
    const {groups, onCreate, onUpdate, onDelete, fetchData} = this.props;
    return (
      <div className="row">
        <div className="col-md-12">
          <ul>
            {groups.filter(
              (group: GroupModel) => _.isNil(group.deleted) || !group.deleted
            ).map(
              (group: GroupModel) =>
                <li className="list-item" key={group.uuid}>
                  <Group group={group} onDelete={() => onDelete(group)}/>
                </li>)}
          </ul>
        </div>
      </div>
    );
  }
}
