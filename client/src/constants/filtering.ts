import { FilterOption } from '../interfaces/filterOptions';

export const FILTER_EXAMPLES: { [key: string]: (value: string) => string } = {
  datetime: (value: string): string =>
    `${value}: >=2018-10-01 or ${value}: ~2018-10-01 or ${value}: 2018-10-01 .. 2019-10-01`,
  scalar: (value: string) => `${value}: 0.1 or ${value}: >0.1 or ${value}: ~0.1`,
  int: (value: string) => `${value}: 3 or ${value}: >2 or ${value}: ~5`,
  id: (id: string) => `${id}: 12 or ${id}: 12|23 or ${id}: ~23|24|25`,
  name: (value) => `${value}: name1 or ${value}: name1|name13 or ${value}: ~name2|name12`,
};

export const PROJECT_FILTER_OPTIONS = [
  {
    filter: 'id',
    type: 'value',
    desc: FILTER_EXAMPLES.id('id'),
    icon: 'circle',
  },
  {
    filter: 'created_at',
    type: 'datetime',
    desc: FILTER_EXAMPLES.datetime('created_at'),
    icon: 'clock-o',
  },
  {
    filter: 'updated_at',
    type: 'datetime',
    desc: FILTER_EXAMPLES.datetime('updated_at'),
    icon: 'clock-o',
  },
  {
    filter: 'started_at',
    type: 'datetime',
    desc: FILTER_EXAMPLES.datetime('started_at'),
    icon: 'clock-o',
  },
  {
    filter: 'finished_at',
    type: 'datetime',
    desc: FILTER_EXAMPLES.datetime('finished_at'),
    icon: 'clock-o',
  },
  {
    filter: 'tags',
    type: 'value',
    desc: 'tags: value1 or tags: value1|value2|value3 or tags: ~value1|value2',
    icon: 'tags',
  },
  {
    filter: 'name',
    type: 'value',
    desc: FILTER_EXAMPLES.name('name'),
    icon: 'minus',
  },
  {
    filter: 'user.id',
    type: 'value',
    desc: FILTER_EXAMPLES.id('user.id'),
    icon: 'user-o',
  },
  {
    filter: 'user.username',
    type: 'value',
    desc: FILTER_EXAMPLES.name('user.username'),
    icon: 'user-o',
  }
] as FilterOption[];

export const DEFAULT_FILTER_OPTIONS = [
  ...PROJECT_FILTER_OPTIONS,
  ...[
    // {
    //   filter: 'project.id',
    //   type: 'value',
    //   desc: FILTER_EXAMPLES.datetime('created_at'),
    //   icon: 'server',
    // },
    // {
    //   filter: 'project.name',
    //   type: 'value',
    //   desc: FILTER_EXAMPLES.name('project.name'),
    //   icon: 'server',
    // },
    {
      filter: 'status',
      type: 'value',
      desc: 'status: running or status: succeeded|failed or status: ~started|building',
      icon: 'minus',
    }
  ]
] as FilterOption[];

export const BUILD_FILTER_OPTIONS = [
  ...DEFAULT_FILTER_OPTIONS,
  ...[
    {
      filter: 'commit',
      type: 'value',
      desc: 'commit: 7afbc6aaf1054d4113b4a740396fb861518da044 or commit: hash1|hash2',
      icon: 'hashtag',
    }
  ]
] as FilterOption[];

export const JOB_FILTER_OPTIONS = [
  ...BUILD_FILTER_OPTIONS,
  ...[
    {
      filter: 'build.id',
      type: 'value',
      desc: FILTER_EXAMPLES.id('build.id'),
      icon: 'gavel',
    },
    {
      filter: 'build.name',
      type: 'value',
      desc: FILTER_EXAMPLES.name('build.name'),
      icon: 'gavel',
    },
  ]
] as FilterOption[];
