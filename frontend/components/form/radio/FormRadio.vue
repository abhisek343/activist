<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<template>
  <input
    v-bind="{ ...$attrs, onChange: updateValue }"
    :id="uuid"
    class="field"
    :checked="modelValue === true"
    type="radio"
  />
  <label v-if="label" :for="uuid">
    {{ label }}
  </label>
  <BaseErrorMessage v-if="error" :id="`${uuid}-error`">
    {{ error }}
  </BaseErrorMessage>
</template>

<script setup lang="ts">
import { v4 as uuidv4 } from "uuid";

import useFormInput from "~/composables/useFormSetup";

export interface Props {
  label?: string;
  modelValue?: boolean;
  error?: string;
}

const uuid = uuidv4();

const props = withDefaults(defineProps<Props>(), {
  label: "",
  error: "",
});

const emit = defineEmits(["update:modelValue"]);
const { updateValue } = useFormInput(props, emit);
</script>
