import {field} from 'ember-gen';

function disable_field(el) {
  return field(el, {
    attrs: {
      disabled: true,
    }
  })
}

export {disable_field}
