from typing import Dict, List, Optional


class TagsSerializerMixin(object):

    def validated_tags(self, validated_data: Dict, tags: Optional[List[str]]):
        new_tags = validated_data.get('tags')

        if new_tags:
            new_tags = list(set(new_tags))
            validated_data['tags'] = new_tags

        if not validated_data.get('merge') or not tags or not new_tags:
            # This is the default behavior
            return validated_data

        new_tags = tags + [tag for tag in new_tags if tag not in tags]
        validated_data['tags'] = new_tags
        return validated_data
