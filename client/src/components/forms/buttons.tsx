import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';

export const FormButtons = (cancelUrl: string, isLoading: boolean, configButton: string) => {
  return (
    <div className="form-group form-actions">
      <div className="row">
        <div className="col-md-11">
          <button
            type="submit"
            className="btn btn-success"
            disabled={isLoading}
          >
            {configButton}
          </button>
          <LinkContainer to={`${cancelUrl}#`}>
            <button className="btn btn-default pull-right">cancel</button>
          </LinkContainer>
        </div>
      </div>
    </div>
  );
};
