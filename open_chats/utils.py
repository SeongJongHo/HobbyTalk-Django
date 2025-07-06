class RedisKeyGenerator:
    @staticmethod
    def get_cache_chat_ids_key(open_chat_room_id: int = 0) -> str:
        return f"open_chat_room:{open_chat_room_id}:chats"
    @staticmethod
    def get_chat_key(open_chat_id: int = 0) -> str:
        return f"open_chat:{open_chat_id}"
    @staticmethod
    def get_batch_chat_ids_key() -> str:
        return "open_chat_:batch"
    @staticmethod
    def get_processed_chat_ids_key(id: int = 0) -> str:
        return f"open_chats:{id}:processed"

class LuaScript:

    
    @staticmethod
    def get_char_save_script() -> str:
        return """
            redis.call("RPUSH", KEYS[1], ARGV[1])

            local batch_size = redis.call("RPUSH", KEYS[2], ARGV[1])

            redis.call("SET", KEYS[4], ARGV[2])

            if batch_size >= 1000 then
                redis.call("RENAME", KEYS[2], KEYS[3])

                return {1, KEYS[3]}
            else
                return {0, ""}
            end
        """