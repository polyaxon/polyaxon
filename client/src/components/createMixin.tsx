import * as React from 'react';

import { NameSlug } from '../constants/helpTexts';
import { BaseState } from './forms/baseCeationState';
import MDEdit from './mdEditor/mdEdit';
import Polyaxonfile from './polyaxonfile/polyaxonfile';
import TagsEdit from './tags/tagsEdit';


export class CreateMixin<P extends {}, S extends BaseState = BaseState> extends React.Component<P, S> {
  public update = (dict: { [key: string]: any }): void => { return; };

  public handleTagsChange = (value: Array<{ label: string, value: string }>) => {
    this.update({tags: value});
  };

  public handleReadmeChange = (value: string) => {
    this.update({readme: value});
  };

  public handleDescriptionChange = (description: string) => {
    this.update({description});
  };

  public handleNameChange = (name: string) => {
    this.update({name});
  };

  public handlePolyaxonfileChange = (polyaxonfile: string) => {
    this.update({polyaxonfile});
  };

  public renderName = () => (
    <div className="form-group">
      <label className="col-sm-2 control-label">Name</label>
      <div className="col-sm-5">
        <input
          type="text"
          className="form-control input-sm"
          onChange={(event) => this.handleNameChange(event.target.value)}
        />
        <span id="helpBlock" className="help-block">{NameSlug}</span>
      </div>
    </div>
  );

  public renderDescription = () => (
    <div className="form-group">
      <label className="col-sm-2 control-label">Description</label>
      <div className="col-sm-10">
        <input
          type="text"
          className="form-control input-sm"
          onChange={(event) => this.handleDescriptionChange(event.target.value)}
        />
      </div>
    </div>
  );

  public renderReadme = () => (
    <div className="form-group">
      <label className="col-sm-2 control-label">Read me</label>
      <div className="col-sm-10">
        <MDEdit
          content=""
          handleChange={this.handleReadmeChange}
        />
      </div>
    </div>
  );

  public renderTags = () => (
    <div className="form-group">
      <label className="col-sm-2 control-label">Tags</label>
      <div className="col-sm-10">
        <TagsEdit tags={[]} handleChange={this.handleTagsChange}/>
      </div>
    </div>
  );

  public renderConfig = () => (
    <div className="form-group">
      <label className="col-sm-2 control-label">Config</label>
      <div className="col-sm-10">
        <Polyaxonfile
          content=""
          handleChange={this.handlePolyaxonfileChange}
        />
      </div>
    </div>
  );
}
