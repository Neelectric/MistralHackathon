# Local pixtral wrapper that works with llama_index
# System imports
from typing import Optional, List, Mapping, Any

# External imports
from llama_index.core.llms import (
    CustomLLM,
    CompletionResponse,
    CompletionResponseGen,
    LLMMetadata,
)
from llama_index.core.llms.callbacks import llm_completion_callback

# Local imports
from src.pixtral_prompting import prompt_pixtral_text



class PixtralWrapper(CustomLLM):
    context_window: int = 128000
    num_output: int = 8192 * 4
    dummy_response: str = "My response"

    @property
    def metadata(self) -> LLMMetadata:
        """Get LLM metadata."""
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.num_output,
        )

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        for i in range(5):
            output = prompt_pixtral_text(prompt)
            if output is not None:
                break
        print(output)
        return CompletionResponse(text=output)

    @llm_completion_callback()
    def stream_complete(
        self, prompt: str, **kwargs: Any
    ) -> CompletionResponseGen:
        response = ""
        for token in self.dummy_response:
            response += token
            yield CompletionResponse(text=response, delta=token)