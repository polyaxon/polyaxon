export class PaginationStateSchema {
  public projectCurrentPage: number;
  public groupCurrentPage: number;
  public experimentCurrentPage: number;
  public jobCurrentPage: number;
  public buildCurrentPage: number;
  public experimentJobCurrentPage: number;
}

export const PaginationEmptyState = {
  projectCurrentPage: 1,
  groupCurrentPage: 1,
  experimentCurrentPage: 1,
  jobCurrentPage: 1,
  buildCurrentPage: 1,
  experimentJobCurrentPage: 1,
};
