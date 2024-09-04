import win32api
import win32job

def default_set_memory_limit(memory_limit_mb: int) -> None:
	"""
	Sets the default memory limit for the current process.

	Parameters:
		memory_limit_mb (int): The memory limit in megabytes.

	Returns:
		None
	"""
	hjob = win32job.CreateJobObject(None, "")  # type: win32job.HANDLE
	info = win32job.QueryInformationJobObject(hjob, win32job.JobObjectExtendedLimitInformation)  # type: dict
	info['ProcessMemoryLimit'] = memory_limit_mb * 1024 * 1024 * 1024  # type: int
	info['BasicLimitInformation']['LimitFlags'] |= win32job.JOB_OBJECT_LIMIT_PROCESS_MEMORY  # type: int

	win32job.SetInformationJobObject(hjob, win32job.JobObjectExtendedLimitInformation, info)  # type: None

	hproc = win32api.GetCurrentProcess()  # type: int
	win32job.AssignProcessToJobObject(hjob, hproc)  # type: None

def set_memory_limit(memory_limit_gb: int = 2) -> callable:
	"""
	Sets a memory limit for a given function.

	Args:
		memory_limit_gb (int): The memory limit in GB. Defaults to 2.

	Returns:
		set_memory_limit_wrapper (callable): A decorator that sets the memory limit for a function.

	 Example:
        @set_memory_limit(4)  # Set the memory limit to 4 GB
        def my_memory_intensive_function():
            # Function code here
            pass

        my_memory_intensive_function()  # Run the function with the set memory limit

	 Example:
        @set_memory_limit(8)  # Set the memory limit to 8 GB
        def main():
            # code here

		if __name__ == "__main__":
			main()
	"""
	def set_memory_limit_wrapper(func: callable) -> callable:
		def wrapper(*args, **kwargs):
			if memory_limit_gb <= 0:
				print("Error: Memory limit must be greater than 0.")
				return
			# set memory limit
			hjob = win32job.CreateJobObject(None, "")
			info = win32job.QueryInformationJobObject(hjob, win32job.JobObjectExtendedLimitInformation)
			info['ProcessMemoryLimit'] = memory_limit_gb * 1024 * 1024 * 1024
			info['BasicLimitInformation']['LimitFlags'] |= win32job.JOB_OBJECT_LIMIT_PROCESS_MEMORY

			win32job.SetInformationJobObject(hjob, win32job.JobObjectExtendedLimitInformation, info)

			hproc = win32api.GetCurrentProcess()
			win32job.AssignProcessToJobObject(hjob, hproc)

			# run script
			func(*args, **kwargs)

		return wrapper
	return set_memory_limit_wrapper