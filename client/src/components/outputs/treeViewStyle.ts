export const OUTPUTS_TREE_STYLE = {
  tree: {
    base: {
      listStyle: 'none',
      margin: 0,
      padding: 0,
      fontSize: '14px',
      borderRight: '.1rem solid rgba(0, 0, 0, .07)',
      height: '620px',
      overflow: 'scroll',
    },
    node: {
      base: {
        position: 'relative'
      },
      link: {
        cursor: 'pointer',
        position: 'relative',
        padding: '0px 8px',
        display: 'block'
      },
      activeLink: {
        background: '#eceef3'
      },
      toggle: {
        base: {
          position: 'relative',
          display: 'inline-block',
          verticalAlign: 'top',
          marginLeft: '2px',
          height: '20px',
          width: '20px'
        },
        wrapper: {
          position: 'absolute',
          top: '50%',
          left: '50%',
          margin: '-7px 0 0 -7px',
          height: '14px'
        },
        height: 10,
        width: 10,
        arrow: {
          fill: '#283546',
          strokeWidth: 0
        }
      },
      header: {
        base: {
          display: 'inline-block',
          verticalAlign: 'top',
          color: '#333',
          cursor: 'pointer',
        },
        connector: {
          width: '2px',
          height: '12px',
          borderLeft: 'solid 2px black',
          borderBottom: 'solid 2px black',
          position: 'absolute',
          top: '0px',
          left: '-21px'
        },
        title: {
          lineHeight: '24px',
          verticalAlign: 'middle'
        }
      },
      subtree: {
        listStyle: 'none',
        paddingLeft: '19px'
      },
    }
  }
};
