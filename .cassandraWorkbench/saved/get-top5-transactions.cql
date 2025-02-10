  SELECT row_id, account, amount, attributes_blob, body_blob, category,
  description, metadata_s, tags, transaction_date, vector
  FROM transactions_keyspace.transactions
  LIMIT 5;