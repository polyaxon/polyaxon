import * as React from 'react';

export const ModalFormButtons = (onCancel: () => void, isLoading: boolean, configButton: string) => {
  return (
    <div className="form-group form-actions">
      <div className="row">
        <div className="col-md-12">
          <button
            type="submit"
            className="btn btn-success"
            disabled={isLoading}
          >
            {configButton}
          </button>
          <button
            className="btn btn-default pull-right"
            onClick={(event: any) => {event.preventDefault(); onCancel(); }}
          >
            cancel
          </button>
        </div>
      </div>
    </div>
  );
};
