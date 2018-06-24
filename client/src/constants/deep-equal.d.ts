declare module 'deep-equal' {

  interface DeepEqualOptions {
    strict: boolean;
  }

  let deepEqual: (
    actual: Object,
    expected: Object,
    opts?: DeepEqualOptions) => boolean;

  export = deepEqual;
}
