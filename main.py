# main.py
import asyncio
import json
import logging
import os
from skland_api import SklandAPI

# 日志初始化
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SklandAutoSign")


def _parse_users_from_env() -> list[dict]:
    """从环境变量中（Github里的secret里）读取Token"""
    # 1. 解析多账号 JSON 格式----保留原来项目的留下的功能，一起写了，不过一般多人的话直接用多行Token就行了，教程里没放实际能用
    users_json = os.getenv("SKLAND_USERS_JSON", "").strip()
    if users_json:
        try:
            parsed = json.loads(users_json)
            if isinstance(parsed, list):
                users = []
                for idx, item in enumerate(parsed, 1):
                    if isinstance(item, dict) and item.get("token"):
                        users.append({
                            "nickname": item.get("nickname", f"账号{idx}"),
                            "token": str(item.get("token", "")).strip(),
                        })
                if users: return users
        except Exception as e:
            logger.error(f"解析 SKLAND_USERS_JSON 失败: {e}")

    # 2. 解析多行 Token
    tokens_raw = os.getenv("SKLAND_TOKENS", "").strip()
    if tokens_raw:
        normalized = tokens_raw.replace(",", "\n")
        tokens = [t.strip() for t in normalized.splitlines() if t.strip()]
        if tokens:
            return [{"nickname": f"账号{i}", "token": t} for i, t in enumerate(tokens, 1)]

    # 3. 解析单 Token
    single_token = os.getenv("SKLAND_TOKEN", "").strip()
    if single_token:
        return [{"nickname": "主账号", "token": single_token}]

    return []#什么都没有返回滚木


async def run_sign_in():
    # 关掉底层库中网络请求相关的日志，因为超级多会刷屏
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    users = _parse_users_from_env()
    if not users:#滚木就是没Token
        logger.warning("未发现有效账号，请在 GitHub Secrets 中配置 SKLAND_TOKEN 或 SKLAND_TOKENS")
        return

    api = SklandAPI(max_retries=3)# 初始化SklandAPI，最大重试3次
    logger.info(f"🚀 开始执行签到任务，共计 {len(users)} 个账号")

    # user -> token , index -> 第几个账号 这个类型返回值pair类型为(序号,token)差点搞错了
    for index, user in enumerate(users, 1):
        nickname_cfg = user.get("nickname", "未知用户")
        token = user.get("token")

        logger.info(f"[{index}/{len(users)}] 正在处理账号: {nickname_cfg}")

        if not token:
            logger.error(f"  ❌ [{nickname_cfg}] 滚木Token，跳过")
            continue

        try:
            # 执行签到获取结果
            results, official_nickname = await api.do_full_sign_in(token)

            if not results:
                logger.warning(f"  ⚠️ [{nickname_cfg}] 未找到绑定的《明日方舟》或《终末地》角色")
                continue

            for r in results:
                # 判断是否已经签到过,这个api库会分别跑明日方舟和终末地
                is_signed_already = not r.success and any(k in r.error for k in ["已签到", "重复", "already"])

                if r.success:
                    detail = f" 获得: {', '.join(r.awards)}" if r.awards else ""
                    logger.info(f"  ✅ {r.game}: 签到成功!{detail}")
                elif is_signed_already:
                    logger.info(f"  ✅ {r.game}: 今日已签到过了")
                else:
                    logger.error(f"  ❌ {r.game}: 签到失败 ({r.error})")

        except Exception as e:
            logger.error(f"  ❌ [{nickname_cfg}] 执行异常: {str(e)}")

        # 睡一会儿
        await asyncio.sleep(2)

    await api.close()
    logger.info("🎉 所有账号签到任务执行完毕")


if __name__ == "__main__":
    asyncio.run(run_sign_in())