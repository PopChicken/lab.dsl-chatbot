<template>
  <div v-loading="loading" class="box" :style="boxStyle" element-loading-background="white">
    <div v-if="stage == 0" class="portal">
      <div class="header-bar">
        <div class="name">
          <span class="title">{{ $t('message.cp') }}</span>
        </div>
        <div class="control">
          <span>{{ $t('message.hello') }} {{ username }}</span>
          <el-divider direction="vertical" content-position="center" />
          <span class="logout" @click="logout">{{ $t('message.logout') }}</span>
        </div>
      </div>
      <div class="option">
        <el-select v-model="schema" :placeholder="$t('message.sel_schema')">
          <el-option
            v-for="item in options"
            :key="item.schema"
            :label="item.title"
            :value="item.schema"
          />
        </el-select>
        <el-button @click="submit" style="margin-left: 6px">{{ $t('message.confirm') }}</el-button>
      </div>
    </div>
    <chatbox v-if="stage == 1" :schema="schema" :name="name" :title="title" :am="am" :pm="pm" />
  </div>
</template>

<script lang="ts">
import Chatbox from "@/components/Chatbox.vue";
import { fetchOptions, fetchDetail } from "@/api/portal";
import { onBeforeMount, ref } from "vue";
import { openToast } from "toast-ts";
import { useI18n } from 'vue-i18n'
import { useStore } from '@/store'
import { setToken } from '@/utils/auth';

export default {
  name: "Portal",
  components: {
    Chatbox,
  },
  setup() {
    const stage = ref(0);
    const loading = ref(false);
    const schema = ref("");
    const boxStyle = ref({
    })
    const options: Array<{ schema: string; title: string }> = [];
    const am = ref("AM");
    const pm = ref("PM");
    const name = ref("bot1");
    const title = ref("service");
    const store = useStore()
    const username = store.$state.name
    

    const { t } = useI18n()

    onBeforeMount(async () => {
      loading.value = true;
      const options_ = await fetchOptions();
      options_.forEach((option) => {
        options.push({
          schema: option.schema,
          title: option.title,
        });
      });
      loading.value = false;
    });

    async function submit(): Promise<void> {
      if (schema.value === "") {
        openToast(t('message.sel_schema'));
        return;
      }
      loading.value = true;

      const detail = await fetchDetail({schema: schema.value})
      name.value = detail.name
      title.value = detail.title
      am.value = detail.am
      pm.value = detail.pm

      stage.value = 1
      loading.value = false
    }

    function logout() {
      setToken('')
      location.reload()
    }

    return {
      stage,
      loading,
      schema,
      options,
      boxStyle,
      name,
      title,
      am,
      pm,
      username,
      submit,
      logout
    };
  },
};
</script>

<style lang="scss" scoped>
@media screen and (min-width: 961px) {
  .box {
    position: relative;
    display: flex;
    flex-flow: column;
    width: 500px;
    height: 800px;
    border-radius: 5px;
    background-color: white;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
    align-items: center;
    justify-content: center;
  }
}

@media (max-width: 960px) {
  .box {
    position: relative;
    display: flex;
    flex-flow: column;
    width: 100vw;
    height: 100vh;
    background-color: white;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
    align-items: center;
    justify-content: center;
  }
}

.portal {
  width: 100%;
  height: 100%;

  .header-bar {
    display: flex;
    align-items: center;
    width: 100%;
    height: 80px;
    box-sizing: border-box;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2), 0 0 6px rgba(0, 0, 0, 0.04);

    .name {
      display: flex;
      flex: 0 0 auto;
      margin-left: 20px;
      flex-flow: column;
      font-size: 20px;

      span {
        text-align: left;
      }
    }

    .control::before {
      content: "";
      flex: 1
    }

    .control {
      flex: 2;
      text-align: right;
      margin-left: auto;

      .logout {
        cursor: pointer;
      }
    }
  }

  .option {
    margin-top: 100px;
  }
}
</style>
