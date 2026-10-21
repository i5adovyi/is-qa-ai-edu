# Help AI find the right evidence

A model may know general testing concepts but not your team's current release policy. An application can search approved documents and include relevant passages in the model's input. This is retrieval-augmented generation, or **RAG**. It changes the information available for a response; it does not necessarily retrain the model.

## Follow one question

Someone asks, “Can we release with this failing check?” The application searches the policy collection, retrieves passages, and asks the model to answer using them. The answer depends both on finding the right policy and interpreting it correctly.

Documents are often divided into smaller passages called chunks. An embedding represents content as numbers that can be compared for similarity. A vector search uses those representations to find related content. Keyword search can be better for an exact error code or product identifier; systems may combine both approaches. You do not need to install a vector database to understand this process.

## Test retrieval and the answer separately

If the application retrieved an obsolete release policy, a faithful summary can still be wrong for today's decision. If the correct passage was retrieved but ignored, improving search will not fix the answer. Inspect the question, retrieved sources, source dates, and final response as distinct evidence.

Useful cases include a document that does not exist, two versions with conflicting rules, an exact identifier, and a question outside the collection. The correct behavior might be to say the evidence is insufficient. More retrieved text can add distractions as easily as useful context.

Permissions matter before generation. A user should not receive a private document merely because it is semantically relevant. Filtering a generated answer after the private text has already entered the request is not equivalent to enforcing access during retrieval.

## Citations need checking

A citation is useful only if it points to an accessible source that supports the claim. A real document title attached to an unsupported statement is still a failure. For an SDET, this means checking both source selection and the relationship between the source and the answer.

The Microsoft reading below introduces the mechanics. Its optional build instructions have additional dependencies; you can stop after the explanation. Next, learn how assistants use tools and reusable instructions to work with systems rather than only read documents.
