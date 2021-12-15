<template>
  <div class="box">
    <el-input class="username" v-model="username" :placeholder="$t('message.usrn')"/>
    <el-input class="password" v-model="pwd" :placeholder="$t('message.pwd')" @keyup.enter="submit" show-password/>
    <el-button class="sumbit-btn" style="width: 300px" @click="submit">{{$t('message.sign')}}</el-button>
  </div>
</template>

<script>
import { Sign } from '@/api/sign'
import { ref } from "vue";
import { useI18n } from 'vue-i18n'
import { openToast } from 'toast-ts'
import { useStore } from '@/store'
import { Md5 } from "ts-md5";

export default {
  setup() {
    const username = ref("")
    const pwd = ref("")
    const t = useI18n()['t']
    const store = useStore()

    async function submit() {
      if (username.value.length < 4 || username.value.length > 32) {
        openToast(t('message.usrtext'))
        return
      } else if (/^[a-z0-9A-Z_]+$/.test(username.value) === false) {
        openToast(t('message.illegal_usrn'))
        return
      } else if (pwd.value.length < 8) {
        openToast(t('message.pwdtext'))
        return
      }

      let pwdhash = Md5.hashStr(pwd.value)
      let resp = await Sign({username: username.value, pwd: pwdhash})
      if (resp.code == 0) {
        store.$state.name = username.value
        location.reload()
      } else {
        openToast(t('message.wrongpwd'))
      }
    }

    return {
      username,
      pwd,
      submit
    }
  },
}
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
    padding-top: 240px;
    box-sizing: border-box;
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
    padding-top: 30vh;
    box-sizing: border-box;
  }
}

.username {
  margin-bottom: 10px;
  width: 300px;
}

.password {
  margin-bottom: 30px;
  width: 300px
}
</style>