<template>
  <div class="box">
    <div class="header-bar">
      <el-avatar
        class="avatar"
        shape="square"
        :size="50"
        :src="require('../assets/images/avatar.png')"
      />
      <div class="name">
        <span class="title">{{ this.name }}</span>
        <span class="subtitle">{{ this.title }}</span>
      </div>
    </div>
    <div class="main">
      <el-scrollbar ref="historyScrollbar" class="chat">
        <div
          ref="historyContent"
          style="
            width: 100%;
            height: 100%;
            box-sizing: border-box;
            padding-top: 20px;
          "
        >
          <div
            v-for="msg in history"
            :key="msg.id"
            :class="'message' + ' ' + (msg.bot ? '' : 'user-message')"
          >
            <!--bot side-->
            <el-avatar
              v-if="msg.bot"
              class="avatar"
              style="min-width: 40px"
              shape="circle"
              :size="40"
              :src="require('../assets/images/avatar.png')"
            />
            <div v-if="msg.bot" class="bubble bot-bubble">
              <span>{{ msg.content }}</span>
            </div>
            <div v-if="msg.bot" class="time bot-time">
              <span class="time-upper" />
              <span>{{ time(msg.time) }}</span>
            </div>
            <!--user side-->
            <el-avatar
              v-if="!msg.bot"
              class="avatar"
              style="min-width: 40px"
              shape="circle"
              :size="40"
              :src="require('../assets/images/customer.jpg')"
            />
            <div v-if="!msg.bot" class="bubble user-bubble">
              <span>{{ msg.content }}</span>
            </div>
            <div v-if="!msg.bot" class="time user-time">
              <span class="time-upper" />
              <span>{{ time(msg.time) }}</span>
            </div>
          </div>
        </div>
      </el-scrollbar>
    </div>
    <div class="control-bar">
      <el-input :disabled="disabled" v-model="message" @keyup.enter="send()" />
      <el-button
        @click="send()"
        :disabled="disabled"
        class="send-btn"
        type="primary"
        circle
        >發</el-button
      >
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue-demi";
import { fetchInit, fetchMessage } from "@/api/chat";
import { openToast } from "toast-ts";
import { useI18n } from "vue-i18n";

export default defineComponent({
  data() {
    return {
      disabled: false,
      message: "",
      maxMsgId: 0,
      history: [] as any,
    };
  },
  setup() {
    const { t } = useI18n();
    return {
      t,
    };
  },
  props: {
    name: { type: String, default: "" },
    title: { type: String, default: "" },
    am: { type: String, default: "" },
    pm: { type: String, default: "" },
    error: { type: String, default: "" },
    schema: { type: String, default: "" },
  },
  async mounted() {
    let fail = false;
    let resp;
    try {
      resp = await fetchInit({ schema: this.schema });
      if (resp.code != 0) {
        fail = true;
      }
    } catch (error) {
      console.error(error);
      fail = true;
    }

    if (resp === undefined) {
      openToast(this.t('message.error'));
      return;
    }

    if (fail) {
      this.disabled = true;
      this.message = this.t('message.service_err');
      return;
    }

    let msgList = resp.data;

    msgList.forEach((msg) => {
      this.loadMsg(true, msg.content, msg.time);
    });
  },
  methods: {
    async loadMsg(bot: boolean, msg: string, time: number) {
      this.history.push({
        msg_id: this.maxMsgId++,
        bot: bot,
        content: msg,
        time: time,
      });
      await this.$nextTick();
      let historyContent = this.$refs.historyContent as any;
      let historyScrollbar = this.$refs.historyScrollbar as any;
      historyScrollbar.setScrollTop(historyContent.clientHeight);
    },
    zero(num: number) {
      return num < 10 ? "0" + num : num;
    },
    time(timestamp: number) {
      const date: Date = new Date(timestamp);
      let h: number = date.getHours();
      let m: number = date.getMinutes();
      return (
        this.zero(h) + ":" + this.zero(m) + " " + (h >= 12 ? this.pm : this.am)
      );
    },
    async send() {
      let msg: string = this.message;
      if (msg.length == 0) {
        return;
      }
      let time: number = new Date().getTime();
      this.message = "";
      this.loadMsg(false, msg, time);

      try {
        let resp = await fetchMessage({
          content: msg,
        });

        if (resp.code == 2) {
          msg = this.t('message.expire');
          time = new Date().getTime();
          this.loadMsg(true, msg, time);
        } else if (resp.code != 0) {
          msg = this.error;
          time = new Date().getTime();
          this.loadMsg(true, msg, time);
        } else {
          let data = resp.data;
          data.forEach((elem) => {
            this.loadMsg(true, elem.content, elem.time);
          });
        }
      } catch (error) {
        console.error(error);
        msg = this.error;
        time = new Date().getTime();
        this.loadMsg(true, msg, time);
      }
    },
  },
});
</script>

<style lang="scss" scoped>
.header-bar {
  display: flex;
  align-items: center;
  width: 100%;
  height: 80px;
  box-sizing: border-box;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2), 0 0 6px rgba(0, 0, 0, 0.04);

  .avatar {
    flex: 0 0 auto;
  }

  .name {
    display: flex;
    flex: 0 0 auto;
    margin-left: 20px;
    flex-flow: column;
    font-size: 20px;

    span {
      text-align: left;
    }

    .title {
    }

    .subtitle {
      font-size: 14px;
      color: #8f8f8f;
    }
  }
}

.main {
  position: relative;
  flex: 1;
  width: 100%;
  overflow-y: auto;

  .chat {
    height: 100%;
    padding: 0 20px 0;

    .message {
      display: flex;
      padding: 0 0 20px;
      width: 100%;
      text-align: left;
    }

    .user-message {
      flex-flow: row-reverse;
    }

    .bubble {
      position: relative;
      width: auto;
      padding: 10px;
      background: #f07c82;
      -moz-border-radius: 10px;
      -webkit-border-radius: 10px;
      border-radius: 10px;

      span {
        white-space: pre-wrap;
        word-break: break-word;
      }
    }

    .bot-bubble::before {
      content: "";
      position: absolute;
      width: 0;
      height: 0;
      border-top: 13px solid transparent;
      border-right: 26px solid #f07c82;
      border-bottom: 13px solid transparent;
      margin: -3px 0 0 -25px;
    }

    .bot-bubble {
      margin-left: 25px;
    }

    .user-bubble::after {
      content: "";
      position: absolute;
      top: 0;
      right: 0;
      width: 0;
      height: 0;
      border-top: 13px solid transparent;
      border-left: 26px solid #ed5a65;
      border-bottom: 13px solid transparent;
      margin: 6px -15px 0 0;
    }

    .user-bubble {
      margin-right: 25px;
      background-color: #ed5a65;
    }

    .time {
      position: relative;
      display: flex;
      flex-flow: column;
      min-width: 70px;

      .time-upper {
        flex: 1;
      }

      span {
        color: #c7c7c7;
        font-size: 14px;
      }
    }

    .bot-time span {
      margin-left: 5px;
    }

    .user-time span {
      margin-right: 5px;
    }
  }
}

.control-bar {
  display: flex;
  flex-flow: row;
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
  padding: 0 20px;
  width: 100%;
  height: 80px;
  border-top: 1px solid #c7c7c7;

  .el-input :deep(.el-input__inner) {
    border-radius: 20px;
  }

  .send-btn {
    margin-left: 20px;
  }
}
</style>