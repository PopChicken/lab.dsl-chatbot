import request from '@/utils/request'

export async function fetchOptions(): Promise<Array<{ schema: string; title: string} >> {
  const resp = await request({
    url: '/api/bot/portal/option',
    method: 'get'
  })
  return resp.data
}

export async function fetchDetail(data: { schema: string }): Promise<{
  name: string,
  title: string,
  welcome: string,
  subservice: string,
  option: string,
  am: string,
  pm: string,
  cancel: string,
  cancel_info: string,
  cancel_success: string,
  back: string,
  back_info: string,
  back_success: string,
  other: string,
  unkown: string,
  error: string,
}> {
  const resp = await request({
    url: '/api/bot/portal/detail',
    method: 'post',
    data
  })
  return resp.data
}