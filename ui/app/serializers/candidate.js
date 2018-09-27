import DS from 'ember-data';
import Serializer from './application';

const embedded = { embedded: 'always' };

export default Serializer.extend(DS.EmbeddedRecordsMixin, {
  attrs: {
    id_passport_file: embedded,
    cv: embedded,
    diplomas: embedded,
    publications: embedded,
    pubs_note: embedded,
  }
});
