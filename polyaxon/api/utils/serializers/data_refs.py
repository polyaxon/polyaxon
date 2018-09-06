class DataRefsSerializerMixin(object):

    def validated_data_refs(self, validated_data, data_refs):
        new_data_refs = validated_data.get('data_refs')
        if not validated_data.get('merge') or not data_refs or not new_data_refs:
            # This is the default behavior
            return validated_data

        data_refs.update(new_data_refs)
        validated_data['data_refs'] = data_refs
        return validated_data
