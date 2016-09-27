import Mirage from 'ember-cli-mirage';

const MODELS = [/*'managers'*/];

export default function() {

  for (let model of MODELS) {
    let related = [];
    if (Ember.isArray(model)) {
      [model, related] = model;
    }
    let collection = `/${model}`;
    let item = `/${model}/:id`;

    this.get(collection);
    this.post(collection);
    this.get(item);
    this.put(item);
    this.patch(item);

    this.del(item, function(schema, request) {
      let id = request.params.id;
      let record = schema[model].find(id);

      for (let rel of related) {
        let ref = record.modelName + 'Id';
        let query = {};
        query[ref] = parseInt(id);
        let rels = schema[rel].where(query);
        rels.destroy();
      }
      record.destroy();
    });
  }

  this.get('countries');
};
