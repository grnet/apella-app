import DS from 'ember-data';
import Serializer from './application';

const embedded = { embedded: 'always' };

export default Serializer.extend(DS.EmbeddedRecordsMixin, {
  attrs: {
    self_evaluation_report: embedded,
    statement_file: embedded,
    attachment_files: embedded,
    cv: embedded,
    diplomas: embedded,
    publications: embedded
  }
});
