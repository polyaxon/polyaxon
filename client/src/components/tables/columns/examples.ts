export const FILTER_EXAMPLES: { [key: string]: (value: string) => string } = {
  datetime: (value: string): string =>
    `${value}: >=2018-10-01 or ${value}: ~2018-10-01 or ${value}: 2018-10-01 .. 2019-10-01`,
  scalar: (value: string) => `${value}: 0.1 or ${value}: >0.1 or ${value}: ~0.1`,
  int: (value: string) => `${value}: 3 or ${value}: >2 or ${value}: ~5`,
  id: (id: string) => `${id}: 12 or ${id}: 12|23 or ${id}: ~23|24|25`,
  name: (value) => `${value}: name1 or ${value}: name1|name13 or ${value}: ~name2|name12`,
};
