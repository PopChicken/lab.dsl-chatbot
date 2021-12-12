import request from '@/utils/request'

export async function fetchInit(data: { schema: string }): Promise<{code: number, msg: number, data: Array<{ content: string; time: number }>}> {
  const resp = await request({
    url: '/api/bot/chat/init',
    method: 'post',
    data
  }) as never
  return resp
}

export async function fetchMessage(data: { content: string }): Promise<{code: number, msg: number, data: Array<{ content: string; time: number }>}> {
  const resp = await request({
    url: '/api/bot/chat/message',
    method: 'post',
    data
  }) as never
  return resp
}