"""
FreeRTOS 模块类型定义
基于 freertos_mod.c 转换而来
"""

from typing import Any, Optional, Union, Callable
from micropython import const

# 常量定义
tskIDLE_PRIORITY: int
tskNO_AFFINITY: int
taskSCHEDULER_SUSPENDED: int
taskSCHEDULER_NOT_STARTED: int
taskSCHEDULER_RUNNING: int
pdFALSE: int
pdTRUE: int
pdPASS: int
pdFAIL: int
errQUEUE_EMPTY: int
errQUEUE_FULL: int
errCOULD_NOT_ALLOCATE_REQUIRED_MEMORY: int
errQUEUE_BLOCKED: int
errQUEUE_YIELD: int

# portmacro 常量
portMAX_DELAY: int
portCRITICAL_NESTING_IN_TCB: int
portSTACK_GROWTH: int
portTICK_PERIOD_MS: int
portBYTE_ALIGNMENT: int
portTICK_TYPE_IS_ATOMIC: int

# atomic 常量
ATOMIC_COMPARE_AND_SWAP_SUCCESS: int
ATOMIC_COMPARE_AND_SWAP_FAILURE: int

# 任务状态枚举
eRunning: int
eReady: int
eBlocked: int
eSuspended: int
eDeleted: int
eInvalid: int

# 通知动作枚举
eNoAction: int
eSetBits: int
eIncrement: int
eSetValueWithOverwrite: int
eSetValueWithoutOverwrite: int

# 睡眠模式状态枚举
eAbortSleep: int
eStandardSleep: int
eNoTasksWaitingTimeout: int

# 原子操作函数
def ATOMIC_ENTER_CRITICAL() -> None:
    """进入原子临界区"""
    ...

def ATOMIC_EXIT_CRITICAL() -> None:
    """退出原子临界区"""
    ...

# 任务通知函数
def xTaskNotifyGive(task_handle: Any) -> int:
    """
    任务通知函数
    参数:
        task_handle (Any): 任务句柄
    返回:
        (int): 操作结果
    """
    ...

def xTaskNotifyGiveIndexed(task_handle: Any, index: int) -> int:
    """
    带索引的任务通知函数
    参数:
        task_handle (Any): 任务句柄
        index (int): 通知索引
    返回:
        (int): 操作结果
    """
    ...

def vTaskNotifyGiveFromISR(task_handle: Any, higher_priority_task_woken: Any) -> None:
    """
    从中断服务程序发送任务通知
    参数:
        task_handle (Any): 任务句柄
        higher_priority_task_woken (Any): 高优先级任务唤醒标志
    返回:
        (None): 无返回值
    """
    ...

def ulTaskNotifyTake(clear_bits_on_exit: bool, timeout: int) -> int:
    """
    等待任务通知
    参数:
        clear_bits_on_exit (bool): 退出时是否清除位
        timeout (int): 超时时间
    返回:
        (int): 通知值
    """
    ...

def xTaskNotify(task_handle: Any, value: int, action: int) -> int:
    """
    发送任务通知
    参数:
        task_handle (Any): 任务句柄
        value (int): 通知值
        action (int): 通知动作
    返回:
        (int): 操作结果
    """
    ...

def xTaskNotifyWait(bits_to_clear_on_entry: int, bits_to_clear_on_exit: int, 
                   notification_value: Any, timeout: int) -> int:
    """
    等待任务通知
    参数:
        bits_to_clear_on_entry (int): 进入时清除的位
        bits_to_clear_on_exit (int): 退出时清除的位
        notification_value (Any): 通知值指针
        timeout (int): 超时时间
    返回:
        (int): 操作结果
    """
    ...

# 定时器函数
def xTimerCreateStatic(timer_name: str, period: int, auto_reload: bool, 
                      timer_id: Any, timer_callback: Callable, 
                      timer_buffer: Any) -> Any:
    """
    创建静态定时器
    参数:
        timer_name (str): 定时器名称
        period (int): 定时器周期
        auto_reload (bool): 是否自动重载
        timer_id (Any): 定时器ID
        timer_callback (Callable): 定时器回调函数
        timer_buffer (Any): 定时器缓冲区
    返回:
        (Any): 定时器句柄
    """
    ...

def xTimerStart(timer_handle: Any, timeout: int) -> int:
    """
    启动定时器
    参数:
        timer_handle (Any): 定时器句柄
        timeout (int): 超时时间
    返回:
        (int): 操作结果
    """
    ...

def xTimerStop(timer_handle: Any, timeout: int) -> int:
    """
    停止定时器
    参数:
        timer_handle (Any): 定时器句柄
        timeout (int): 超时时间
    返回:
        (int): 操作结果
    """
    ...

def xTimerDelete(timer_handle: Any, timeout: int) -> int:
    """
    删除定时器
    参数:
        timer_handle (Any): 定时器句柄
        timeout (int): 超时时间
    返回:
        (int): 操作结果
    """
    ...

# 任务函数
def xTaskCreateStatic(task_function: Callable, task_name: str, stack_depth: int,
                     task_parameter: Any, priority: int, stack_buffer: Any,
                     task_buffer: Any) -> Any:
    """
    创建静态任务
    参数:
        task_function (Callable): 任务函数
        task_name (str): 任务名称
        stack_depth (int): 栈深度
        task_parameter (Any): 任务参数
        priority (int): 任务优先级
        stack_buffer (Any): 栈缓冲区
        task_buffer (Any): 任务缓冲区
    返回:
        (Any): 任务句柄
    """
    ...

def vTaskDelete(task_handle: Any) -> None:
    """
    删除任务
    参数:
        task_handle (Any): 任务句柄
    返回:
        (None): 无返回值
    """
    ...

def vTaskDelay(ticks: int) -> None:
    """
    任务延时
    参数:
        ticks (int): 延时时钟数
    返回:
        (None): 无返回值
    """
    ...

def xTaskDelayUntil(previous_wake_time: Any, time_increment: int) -> int:
    """
    任务延时直到指定时间
    参数:
        previous_wake_time (Any): 上次唤醒时间
        time_increment (int): 时间增量
    返回:
        (int): 操作结果
    """
    ...

def uxTaskPriorityGet(task_handle: Any) -> int:
    """
    获取任务优先级
    参数:
        task_handle (Any): 任务句柄
    返回:
        (int): 任务优先级
    """
    ...

def vTaskPrioritySet(task_handle: Any, new_priority: int) -> None:
    """
    设置任务优先级
    参数:
        task_handle (Any): 任务句柄
        new_priority (int): 新优先级
    返回:
        (None): 无返回值
    """
    ...

def vTaskSuspend(task_handle: Any) -> None:
    """
    挂起任务
    参数:
        task_handle (Any): 任务句柄
    返回:
        (None): 无返回值
    """
    ...

def vTaskResume(task_handle: Any) -> None:
    """
    恢复任务
    参数:
        task_handle (Any): 任务句柄
    返回:
        (None): 无返回值
    """
    ...

def vTaskStartScheduler() -> None:
    """
    启动调度器
    参数:
        无
    返回:
        (None): 无返回值
    """
    ...

def vTaskEndScheduler() -> None:
    """
    结束调度器
    参数:
        无
    返回:
        (None): 无返回值
    """
    ...

def xTaskGetTickCount() -> int:
    """
    获取系统时钟计数
    参数:
        无
    返回:
        (int): 系统时钟计数
    """
    ...

def uxTaskGetNumberOfTasks() -> int:
    """
    获取任务数量
    参数:
        无
    返回:
        (int): 任务数量
    """
    ...

# 队列函数
def xQueueCreateStatic(queue_length: int, item_size: int, queue_buffer: Any,
                      queue_struct: Any) -> Any:
    """
    创建静态队列
    参数:
        queue_length (int): 队列长度
        item_size (int): 项目大小
        queue_buffer (Any): 队列缓冲区
        queue_struct (Any): 队列结构
    返回:
        (Any): 队列句柄
    """
    ...

def xQueueSend(queue_handle: Any, item_to_queue: Any, timeout: int) -> int:
    """
    发送数据到队列
    参数:
        queue_handle (Any): 队列句柄
        item_to_queue (Any): 要发送的数据
        timeout (int): 超时时间
    返回:
        (int): 操作结果
    """
    ...

def xQueueReceive(queue_handle: Any, buffer: Any, timeout: int) -> int:
    """
    从队列接收数据
    参数:
        queue_handle (Any): 队列句柄
        buffer (Any): 接收缓冲区
        timeout (int): 超时时间
    返回:
        (int): 操作结果
    """
    ...

def uxQueueMessagesWaiting(queue_handle: Any) -> int:
    """
    获取队列中等待的消息数量
    参数:
        queue_handle (Any): 队列句柄
    返回:
        (int): 消息数量
    """
    ...

def vQueueDelete(queue_handle: Any) -> None:
    """
    删除队列
    参数:
        queue_handle (Any): 队列句柄
    返回:
        (None): 无返回值
    """
    ...

# 信号量函数
def xSemaphoreCreateBinaryStatic(semaphore_buffer: Any) -> Any:
    """
    创建静态二值信号量
    参数:
        semaphore_buffer (Any): 信号量缓冲区
    返回:
        (Any): 信号量句柄
    """
    ...

def xSemaphoreTake(semaphore_handle: Any, timeout: int) -> int:
    """
    获取信号量
    参数:
        semaphore_handle (Any): 信号量句柄
        timeout (int): 超时时间
    返回:
        (int): 操作结果
    """
    ...

def xSemaphoreGive(semaphore_handle: Any) -> int:
    """
    释放信号量
    参数:
        semaphore_handle (Any): 信号量句柄
    返回:
        (int): 操作结果
    """
    ...

def vSemaphoreDelete(semaphore_handle: Any) -> None:
    """
    删除信号量
    参数:
        semaphore_handle (Any): 信号量句柄
    返回:
        (None): 无返回值
    """
    ...

# 事件组函数
def xEventGroupCreateStatic(event_group_buffer: Any) -> Any:
    """
    创建静态事件组
    参数:
        event_group_buffer (Any): 事件组缓冲区
    返回:
        (Any): 事件组句柄
    """
    ...

def xEventGroupWaitBits(event_group: Any, bits_to_wait_for: int, 
                       clear_on_exit: bool, wait_for_all_bits: bool,
                       timeout: int) -> int:
    """
    等待事件组位
    参数:
        event_group (Any): 事件组句柄
        bits_to_wait_for (int): 等待的位
        clear_on_exit (bool): 退出时是否清除
        wait_for_all_bits (bool): 是否等待所有位
        timeout (int): 超时时间
    返回:
        (int): 事件组位值
    """
    ...

def xEventGroupSetBits(event_group: Any, bits_to_set: int) -> int:
    """
    设置事件组位
    参数:
        event_group (Any): 事件组句柄
        bits_to_set (int): 要设置的位
    返回:
        (int): 操作结果
    """
    ...

def xEventGroupClearBits(event_group: Any, bits_to_clear: int) -> int:
    """
    清除事件组位
    参数:
        event_group (Any): 事件组句柄
        bits_to_clear (int): 要清除的位
    返回:
        (int): 操作结果
    """
    ...

def vEventGroupDelete(event_group: Any) -> None:
    """
    删除事件组
    参数:
        event_group (Any): 事件组句柄
    返回:
        (None): 无返回值
    """
    ...

# 流缓冲区函数
def xStreamBufferCreateStatic(buffer_size_bytes: int, trigger_level_bytes: int,
                             is_message_buffer: bool, buffer_storage: Any,
                             stream_buffer_struct: Any) -> Any:
    """
    创建静态流缓冲区
    参数:
        buffer_size_bytes (int): 缓冲区大小字节数
        trigger_level_bytes (int): 触发级别字节数
        is_message_buffer (bool): 是否为消息缓冲区
        buffer_storage (Any): 缓冲区存储
        stream_buffer_struct (Any): 流缓冲区结构
    返回:
        (Any): 流缓冲区句柄
    """
    ...

def xStreamBufferSend(stream_buffer: Any, data: Any, data_length_bytes: int,
                     timeout: int) -> int:
    """
    发送数据到流缓冲区
    参数:
        stream_buffer (Any): 流缓冲区句柄
        data (Any): 要发送的数据
        data_length_bytes (int): 数据长度字节数
        timeout (int): 超时时间
    返回:
        (int): 发送的字节数
    """
    ...

def xStreamBufferReceive(stream_buffer: Any, data: Any, buffer_length_bytes: int,
                        timeout: int) -> int:
    """
    从流缓冲区接收数据
    参数:
        stream_buffer (Any): 流缓冲区句柄
        data (Any): 接收缓冲区
        buffer_length_bytes (int): 缓冲区长度字节数
        timeout (int): 超时时间
    返回:
        (int): 接收的字节数
    """
    ...

def vStreamBufferDelete(stream_buffer: Any) -> None:
    """
    删除流缓冲区
    参数:
        stream_buffer (Any): 流缓冲区句柄
    返回:
        (None): 无返回值
    """
    ...

# 消息缓冲区函数
def xMessageBufferCreateStatic(buffer_size_bytes: int, buffer_storage: Any,
                              message_buffer_struct: Any) -> Any:
    """
    创建静态消息缓冲区
    参数:
        buffer_size_bytes (int): 缓冲区大小字节数
        buffer_storage (Any): 缓冲区存储
        message_buffer_struct (Any): 消息缓冲区结构
    返回:
        (Any): 消息缓冲区句柄
    """
    ...

def xMessageBufferSend(message_buffer: Any, data: Any, data_length_bytes: int,
                      timeout: int) -> int:
    """
    发送数据到消息缓冲区
    参数:
        message_buffer (Any): 消息缓冲区句柄
        data (Any): 要发送的数据
        data_length_bytes (int): 数据长度字节数
        timeout (int): 超时时间
    返回:
        (int): 发送的字节数
    """
    ...

def xMessageBufferReceive(message_buffer: Any, data: Any, buffer_length_bytes: int,
                         timeout: int) -> int:
    """
    从消息缓冲区接收数据
    参数:
        message_buffer (Any): 消息缓冲区句柄
        data (Any): 接收缓冲区
        buffer_length_bytes (int): 缓冲区长度字节数
        timeout (int): 超时时间
    返回:
        (int): 接收的字节数
    """
    ...

def vMessageBufferDelete(message_buffer: Any) -> None:
    """
    删除消息缓冲区
    参数:
        message_buffer (Any): 消息缓冲区句柄
    返回:
        (None): 无返回值
    """
    ...

# 端口宏函数
def portNOP() -> None:
    """
    空操作
    参数:
        无
    返回:
        (None): 无返回值
    """
    ...

def xPortInIsrContext() -> bool:
    """
    检查是否在中断上下文中
    参数:
        无
    返回:
        (bool): 是否在中断上下文中
    """
    ...

def vPortAssertIfInISR() -> None:
    """
    如果在中断中则断言
    参数:
        无
    返回:
        (None): 无返回值
    """
    ...

def vPortEnterCritical() -> None:
    """
    进入临界区
    参数:
        无
    返回:
        (None): 无返回值
    """
    ...

def vPortExitCritical() -> None:
    """
    退出临界区
    参数:
        无
    返回:
        (None): 无返回值
    """
    ...

def vPortYield() -> None:
    """
    让出CPU
    参数:
        无
    返回:
        (None): 无返回值
    """
    ...

def xPortGetTickRateHz() -> int:
    """
    获取时钟频率
    参数:
        无
    返回:
        (int): 时钟频率
    """
    ...

def xPortGetCoreID() -> int:
    """
    获取核心ID
    参数:
        无
    返回:
        (int): 核心ID
    """
    ...

# 项目定义函数
def pdMS_TO_TICKS(x_time_in_ms: int) -> int:
    """
    毫秒转换为时钟数
    参数:
        x_time_in_ms (int): 毫秒数
    返回:
        (int): 时钟数
    """
    ...

def pdTICKS_TO_MS(x_ticks: int) -> int:
    """
    时钟数转换为毫秒
    参数:
        x_ticks (int): 时钟数
    返回:
        (int): 毫秒数
    """
    ...

# IDF 附加函数
def xTaskCreateStaticPinnedToCore(task_function: Callable, task_name: str,
                                 stack_depth: int, task_parameter: Any,
                                 priority: int, stack_buffer: Any,
                                 task_buffer: Any, core_id: int) -> Any:
    """
    创建静态任务并绑定到指定核心
    参数:
        task_function (Callable): 任务函数
        task_name (str): 任务名称
        stack_depth (int): 栈深度
        task_parameter (Any): 任务参数
        priority (int): 任务优先级
        stack_buffer (Any): 栈缓冲区
        task_buffer (Any): 任务缓冲区
        core_id (int): 核心ID
    返回:
        (Any): 任务句柄
    """
    ...

def xTaskGetCoreID() -> int:
    """
    获取当前任务的核心ID
    参数:
        无
    返回:
        (int): 核心ID
    """
    ... 