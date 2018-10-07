import * as sanitize from 'sanitize-html';
import * as Showdown from 'showdown';

export const getConverter = (): Showdown.Converter => {
  const converter = new Showdown.Converter();
  converter.setFlavor('github');
  return converter;
};

export const sanitizeHtml = (value: string) => {
  const compactMD = {
    allowedTags: [
      'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8',
      'blockquote', 'p', 'a', 'ul', 'ol', 'nl', 'li', 'ins',
      'b', 'i', 'strong', 'em', 'strike', 'code', 'hr', 'br', 'div',
      'table', 'thead', 'tbody', 'tr', 'th', 'td',
      'pre', 'del', 'sup', 'sub', 'dl', 'dt', 'dd', 'kbd', 'q',
      'samp', 'var', 'hr', 'rt', 'rp', 'summary', 'img', 'caption', 'figure'],
    allowedAttributes: {
      a: ['href', 'name', 'target'],
      img: ['src', 'longdesc'],
      div: ['itemscope', 'itemtype']
    }
  };
  return sanitize(value, compactMD);
};
